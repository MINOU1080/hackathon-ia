import streamlit as st
from PIL import Image

class View:
    def __init__(self, controller):
        self.controller = controller

    def display(self):
        """Affiche l’interface utilisateur."""
        st.title("Voice Reco")

        img = Image.open("image/logo.png")
        st.image(img, width=200)

        if st.button("Record"):
            message = self.controller.handle_record()
            st.text(message)
