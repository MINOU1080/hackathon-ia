from datetime import datetime
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

from google.cloud import texttospeech, speech
import streamlit as st
import sounddevice as sd
import wavio
import soundfile as sf

class Model:
    def record_voice(self) -> str:
        duration = 5 ######################### a changer ########################   
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


    def text_to_speech(self, txt: str) -> str:
        client = texttospeech.TextToSpeechClient()

        text_input = texttospeech.SynthesisInput(text=txt)

        voice = texttospeech.VoiceSelectionParams(language_code="fr-BE", ssml_gender=texttospeech.SsmlVoiceGender.MALE)

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)

        output_dir = "data/output"
        output_file_path = os.path.join(output_dir, "output.mp3")

        with open(output_file_path, "wb") as f:
            f.write(response.audio_content)

    def speech_to_text(self, input_file: str) -> str:
        client = speech.SpeechClient()

        with open(input_file, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())

        config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code="fr-BE")

        response = client.recognize(config=config, audio=audio)

        transcripts = []
        for result in response.results:
            text = result.alternatives[0].transcript
            transcripts.append(text)

        # Retourner tout le texte concaténé
        return " ".join(transcripts)