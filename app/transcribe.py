import io
import tempfile
import logging
import whisper

# Configure logging
logging.basicConfig(level=logging.INFO)


class Transcribe:
    def __init__(self) -> None:
        logging.info('Initializing Transcribe class and loading Whisper model.')
        self.model = whisper.load_model("medium.en")
        self.options = whisper.DecodingOptions(fp16=False)

    def process_audio(self, audio_file: io.BytesIO) -> str:
        try:
            logging.info('Processing audio for transcription.')
            with tempfile.NamedTemporaryFile() as tmp:
                logging.info('Writing audio data to temporary file.')
                tmp.write(audio_file.read())

                logging.info('Starting transcription using Whisper.')
                result = self.model.transcribe(tmp.name)

            logging.info('Transcription completed. Returning text.')
            logging.info(result)
            return result
        except Exception as e:
            logging.error(f'An error occurred during transcription: {str(e)}')
            return str(e)
