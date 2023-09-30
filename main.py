from flask import Flask
from app.audio_transcription import transcription_blueprint
from app.diarization import diarization_blueprint
from app.text_analysis import analysis_blueprint

app = Flask(__name__)
app.register_blueprint(transcription_blueprint)
app.register_blueprint(diarization_blueprint)
app.register_blueprint(analysis_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
