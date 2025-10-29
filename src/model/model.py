import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

from google.cloud import texttospeech, speech
import streamlit as st

class Model:
    def record_audio(self):
        """Simule un enregistrement audio."""
        self.last_message = "You did press the button"
        return self.last_message
    
    def text_to_speech(self, txt: str) -> str:
        client = texttospeech.TextToSpeechClient()

        text_input = texttospeech.SynthesisInput(text=txt)

        voice = texttospeech.VoiceSelectionParams(language_code="fr-BE", ssml_gender=texttospeech.SsmlVoiceGender.MALE)

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)

        with open("output.mp3", "wb") as f:
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
            print("Transcript:", text)      # pour debug dans console
            st.text(text)                   # pour afficher dans Streamlit
            transcripts.append(text)

        # Retourner tout le texte concaténé
        return " ".join(transcripts)