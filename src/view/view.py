import streamlit as st
from PIL import Image

class View:
    def __init__(self):
        pass

    def display(self):
        """Affiche l’interface utilisateur."""
        st.title("Voice Reco")

        img = Image.open("image/logo.png")
        st.image(img, width=200)

        if st.button("Record"):
            st.text("test")
