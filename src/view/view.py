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

    def get_btn_is_pressed(self): return self.btn_is_pressed

    def display(self):
        """Affiche l'interface utilisateur."""
        st.title("Voice Reco")

        img = Image.open("image/logo.png")
        st.image(img, width=200)

        if st.button("Record"):
            self.btn_is_pressed = True
