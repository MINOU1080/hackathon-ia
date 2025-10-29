from asyncio import sleep
import streamlit as st
from model.model import Model

class Controller:
    def __init__(self):
        self.model = Model()

    def handle_record(self):
        """Appelle le modèle pour enregistrer le son."""
        self.model.text_to_speech("bonjour, comment sa va ?") #####

        transcript = self.model.speech_to_text("output.mp3")
        st.write("Texte complet :", transcript)

        return self.model.record_audio()
