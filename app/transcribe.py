import io
import tempfile

import pyperclip
import whisper


class Transcribe:
    def __init__(self) -> None:
        self.model = whisper.load_model("medium.en") #base")
        self.options = whisper.DecodingOptions(fp16=False)


    def process_audio(_self, audio_file: io.BytesIO) -> str:
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(audio_file.read())
            result = _self.model.transcribe(tmp.name)
        return result["text"] 
