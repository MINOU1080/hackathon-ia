from datetime import datetime
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
import re

from google.cloud import texttospeech, speech
import sounddevice as sd
import soundfile as sf

class Model:
    def record_voice(self) -> str:
        duration = 10
        samplerate = 44100
        channels = 1

        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()

        recordings_dir = os.path.join("data", "recordings")
        os.makedirs(recordings_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(recordings_dir, filename)

        sf.write(filepath, recording, samplerate, subtype='PCM_16')

        return filepath, filename

    def clean_transcript(self, text: str) -> str:
        text = text.replace("*", "")
        text = re.sub(r'\(\s*(…|\.{3,})\s*\)', ' ', text)
        text = re.sub(r'…|\.{3,}', ' ', text)
        text = re.sub(r'([!?.,;:])\1+', r'\1', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text)
        return text
    
    def text_to_speech(self, txt: str, *, clean: bool = True) -> str:
        if txt is not None:
            txt = self.clean_transcript(txt)
        else:
            txt = "Did not understand"

        client = texttospeech.TextToSpeechClient()
        text_input = texttospeech.SynthesisInput(text=txt)

        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-BE",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        response = client.synthesize_speech(
            input=text_input,
            voice=voice,
            audio_config=audio_config
        )

        output_dir = "data/output"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "wb") as f:
            f.write(response.audio_content)

        return output_path

    def speech_to_text(self, input_file: str) -> str:
        client = speech.SpeechClient()
        with open(input_file, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="fr-BE",
            enable_automatic_punctuation=True,
        )
        response = client.recognize(config=config, audio=audio)
        raw = " ".join(r.alternatives[0].transcript for r in response.results)
        # res = self.clean_transcript(raw)  # <-- maintenant défini
        # print(res)
        return raw