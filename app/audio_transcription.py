from flask import Blueprint, request, jsonify, Flask
import logging
import os
from werkzeug.utils import secure_filename
from app.transcribe import Transcribe

transcription_blueprint = Blueprint("transcription", __name__)

transcribe = Transcribe()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'wav','mp3','mp4','mpeg','mpga','m4a','webm'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@transcription_blueprint.route("/transcribe", methods=["POST"])
def transcribe_audio():
    try:
        if 'audio' not in request.files:
            logger.warning('No file part')
            return jsonify({"error": "No audio file provided."}), 400

        file = request.files['audio']

        if file.filename == '':
            logger.warning('No selected file')
            return jsonify({"error": "No selected file."}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # It's a good practice to secure the filename
            transcription = transcribe.process_audio(file)
            return jsonify({"transcription": transcription["text"]}), 200

        else:
            logger.warning(f"Invalid file format: {file.filename}")
            return jsonify({"error": "Invalid file format. Only .wav allowed."}), 400

    except Exception as e:
        logger.exception('Failed to process audio')
        return jsonify({"error": "Failed to process audio."}), 500

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)  # Use an environment variable for debug mode

    app.register_blueprint(transcription_blueprint)

    app.run(debug=app.config['DEBUG'])
