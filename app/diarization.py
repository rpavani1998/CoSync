import datetime
import contextlib
import wave
import io
import numpy as np
from flask import Blueprint, request, jsonify
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
from sklearn.cluster import AgglomerativeClustering
from app.transcribe import Transcribe
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

diarization_blueprint = Blueprint("diarization", __name__)

transcribe = Transcribe()

embedding_model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb")

@diarization_blueprint.route("/diarization", methods=["GET", "POST"])
def diarize_audio():
    try:
        logging.info('Received a request for diarization.')

        if "audio" not in request.files:
            logging.warning('No audio file provided in request.')
            return jsonify({"error": "No audio file provided."}), 400

        audio_file = request.files["audio"]

        if audio_file.filename == "":
            logging.warning('No file selected for audio.')
            return jsonify({"error": "No selected file."}), 400

        num_speakers = int(request.args.get("num_speakers", 2))  
        audio_bytes = io.BytesIO(audio_file.read())

        logging.info('Starting transcription using Whisper.')
        result = transcribe.process_audio(audio_bytes)
        logging.info('result: %s', result)

        segments = result["segments"]
        logging.info('Fetching audio file duration.')
        with contextlib.closing(wave.open(audio_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        audio = Audio()

        def segment_embedding(segment):
            start = segment["start"]
            end = min(duration, segment["end"])
            clip = Segment(start, end)
            audio_file_path = "temp_audio.wav"
            audio_file.save(audio_file_path)
            
            waveform, sample_rate = audio.crop(audio_file_path, clip)
            
            logging.info(f'Segment cropped with shape {waveform.shape} and sample rate {sample_rate}.')
            
            return embedding_model(waveform[None])

        logging.info('Computing embeddings for each segment.')
        embeddings = np.zeros(shape=(len(segments), 192))
        for i, segment in enumerate(segments):
            embeddings[i] = segment_embedding(segment)

        embeddings = np.nan_to_num(embeddings)

        logging.info('Performing speaker diarization using clustering.')
        clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
        labels = clustering.labels_

        for i in range(len(segments)):
            segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

        speaker_segments = []

        logging.info('Assigning speakers to segments and creating response data.')
        for (i, segment) in enumerate(segments):
            if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                speaker_info = {
                    "speaker": segment["speaker"],
                    "start_time": str(time(segment["start"])),
                    "transcription": segment["text"][1:]
                }
                speaker_segments.append(speaker_info)
            else:
                speaker_segments[-1]["transcription"] += ' ' + segment["text"][1:]

        response_data = {"speaker_segments": speaker_segments}

        logging.info('Sending response to client.')
        return jsonify(response_data), 200
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({"error": str(e)}), 500

def time(secs):
    return datetime.timedelta(seconds=round(secs))

if __name__ == "__main__":
    diarization_blueprint.run(debug=True)
