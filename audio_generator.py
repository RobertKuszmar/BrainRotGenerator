from TTS.api import TTS

class AudioGenerator:
    def __init__(self):
        self.tts = TTS("tts_models/en/ek1/tacotron2").to("cuda")
    
    def tts_to_file(self, text: str, file_path: str) -> None:
        self.tts.tts_to_file(text=text, file_path=file_path)