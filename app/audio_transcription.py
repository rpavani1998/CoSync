from flask import Blueprint, request, jsonify
import whisper
from app.transcribe import Transcribe

transcription_blueprint = Blueprint("transcription", __name__)

transcribe = Transcribe()

@transcription_blueprint.route("/transcribe", methods=["GET", "POST"])
def transcribe_audio():
    try:
        # Check if an audio file is included in the request
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided."}), 400

        audio_file = request.files["audio"]

        # Check if the file has a valid format (e.g., WAV)
        if audio_file.filename == "":
            return jsonify({"error": "No selected file."}), 400
        
        transcription = transcribe.process_audio(audio_file)

        return jsonify({"transcription": transcription}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # You can test this module locally by running it as a standalone Flask app
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(transcription_blueprint)

    app.run(debug=True)
