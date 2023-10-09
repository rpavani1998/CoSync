from flask import Blueprint, request, jsonify
import datetime
import subprocess
import torch
import whisper
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from app.transcribe import Transcribe

diarization_blueprint = Blueprint("diarization", __name__)

# Reusing Whisper model used for transcription
transcribe = Transcribe()

# Initialize the speaker embedding model
embedding_model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb")

@diarization_blueprint.route("/diarization", methods=["GET", "POST"])
def diarize_audio():
    try:
        # Check if an audio file is included in the request
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided."}), 400

        audio_file = request.files["audio"]

        # Check if the file has a valid format (e.g., WAV)
        if audio_file.filename == "":
            return jsonify({"error": "No selected file."}), 400

        num_speakers = int(request.args.get("num_speakers", 2))  # Get the number of speakers as a query parameter

        model = transcribe.model

        # Transcribe the audio using Whisper
        result = model.transcribe(audio_file)
        segments = result["segments"]

        # Get the duration of the audio
        with contextlib.closing(wave.open(audio_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        # Initialize the PyAnnote Audio
        audio = Audio()

        # Define the segment embedding function
        def segment_embedding(segment):
            start = segment["start"]
            end = min(duration, segment["end"])
            clip = Segment(start, end)
            waveform, sample_rate = audio.crop(audio_file, clip)
            return embedding_model(waveform[None])

        # Compute embeddings for each segment
        embeddings = np.zeros(shape=(len(segments), 192))
        for i, segment in enumerate(segments):
            embeddings[i] = segment_embedding(segment)

        embeddings = np.nan_to_num(embeddings)

        # Perform speaker diarization using clustering
        clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
        labels = clustering.labels_

        # Assign speakers to segments
        for i in range(len(segments)):
            segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

        speaker_segments = []

        for (i, segment) in enumerate(segments):
            if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                speaker_info = {
                    "speaker": segment["speaker"],
                    "start_time": str(time(segment["start"])),
                    "transcription": segment["text"][1:]
                }
                speaker_segments.append(speaker_info)
            else:
                # Concatenate the text of consecutive segments from the same speaker
                speaker_segments[-1]["transcription"] += ' ' + segment["text"][1:]

        # Create a JSON response containing the speaker diarization segments
        response_data = {
            "speaker_segments": speaker_segments
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def time(secs):
    return datetime.timedelta(seconds=round(secs))

if __name__ == "__main__":
    diarization_blueprint.run(debug=True)
