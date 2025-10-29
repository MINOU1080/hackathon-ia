import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime
import sounddevice as sd
import soundfile as sf


class View:
    def __init__(self):
        self.btn_is_pressed = False
        self.language = "Nerderlands"

    def get_btn_is_pressed(self): return self.btn_is_pressed

    def get_language(self): return self.language

    def display(self):
        """Affiche l'interface utilisateur."""
        # Create a dropdown menu for selecting a hobby
        self.language = st.selectbox("Select a language:", ['Nerderlands', 'French', 'English'])

        st.title("Voice Reco")

        img = Image.open("image/logo.png")
        st.image(img, width=200)

        if st.button("Record"):
            self.btn_is_pressed = True
