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


    # def text_to_speech(self, txt: str) -> str:
    #     client = texttospeech.TextToSpeechClient()

    #     text_input = texttospeech.SynthesisInput(text=txt)

    #     voice = texttospeech.VoiceSelectionParams(language_code="fr-BE", ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    #     audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    #     response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)

    #     output_dir = "data/output"
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"output_{timestamp}.wav"

    #     output_file_path = os.path.join(output_dir, filename)

    #     with open(output_file_path, "wb") as f:
    #         f.write(response.audio_content)

    #     return output_file_path, filename

    # def speech_to_text(self, input_file: str) -> str:
    #     client = speech.SpeechClient()

    #     with open(input_file, "rb") as f:
    #         audio = speech.RecognitionAudio(content=f.read())

    #     config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code="fr-BE")

    #     response = client.recognize(config=config, audio=audio)

    #     transcripts = []
    #     for result in response.results:
    #         text = result.alternatives[0].transcript
    #         transcripts.append(text)

    #     # Retourner tout le texte concaténé
    #     return " ".join(transcripts)

    def text_to_speech(self, txt: str) -> str:
        """Convertit du texte en fichier audio WAV et retourne le chemin du fichier."""
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

        # Crée le dossier data/output s'il n'existe pas
        output_dir = "data/output"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestamp}.wav"
        output_file_path = os.path.join(output_dir, filename)

        # Écrit le fichier audio
        with open(output_file_path, "wb") as f:
            f.write(response.audio_content)

        return output_file_path  # retourne le chemin complet du fichier

    def speech_to_text(self, input_file: str) -> str:
        """Convertit un fichier audio WAV LINEAR16 en texte et retourne la transcription."""
        client = speech.SpeechClient()

        with open(input_file, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="fr-BE"
        )

        response = client.recognize(config=config, audio=audio)

        transcripts = []
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)

        return " ".join(transcripts)