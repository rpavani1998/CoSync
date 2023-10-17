import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flask_cors import CORS

# Importing blueprints
from app.audio_transcription import transcription_blueprint
from app.diarization import diarization_blueprint
from app.text_analysis import analysis_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# App configuration using environment variables as default values
app.config['HOST'] = os.getenv('APP_HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('APP_PORT', 8000))
app.config['DEBUG'] = bool(int(os.getenv('APP_DEBUG', 1)))

# Registering blueprints
blueprints = [transcription_blueprint, diarization_blueprint, analysis_blueprint]
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Logging Configuration
log_level = logging.DEBUG if app.config['DEBUG'] else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File logging handler
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*100, backupCount=10)  # 100MB per logfile, keep 10 old copies
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

# Stream handler to log to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)
logging.getLogger().addHandler(stream_handler)

# Middleware for logging
@app.before_request
def before_request_logging():
    logging.info(f"Request: Endpoint={request.endpoint}, Method={request.method}, Params={request.args}")

# Error handlers
@app.errorhandler(500)
def handle_500_error(e):
    logging.error(f"500 Error: {str(e)}")
    return "Internal Server Error", 500

@app.errorhandler(404)
def handle_404_error(e):
    logging.error(f"404 Error: {str(e)}")
    return "Resource Not Found", 404

# Main entry point
if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
