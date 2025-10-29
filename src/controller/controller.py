from asyncio import sleep
import os
import tempfile
import numpy as np
import streamlit as st
from model.model import Model
from view.view import View
import pandas as pd
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from sentence_transformers import SentenceTransformer


path_fr = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/similar_fr_chunks.json"
path_eng = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_en_2025_09_23/similar_eng_chunks.json"
path_nl = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_nl_2025_09_23/similar_nl_chunks.json"


class Controller:
    def __init__(self,view,auth_controller):
        self.view = View()
        self.model = Model()

    def get_model(self): return self.model

    def get_view(self): return self.view

    def handle_record(self):
        pass
    #     """Appelle le modèle pour enregistrer le son."""
    #     # self.model.text_to_speech("bonjour, comment sa va ?") #####

    #     # transcript = self.model.speech_to_text("output.mp3")
    #     # st.write("Texte complet :", transcript)
    #     input_audio = self.model.record_audio()
        # if self.view.get_btn_is_pressed():
        #     path_input_file, input_file_name = self.model.record_voice()  
        #     input_str = self.model.speech_to_text(path_input_file)
            
        #     texts_dir = "data/texts"
        #     os.makedirs(texts_dir, exist_ok=True)  # crée le dossier si nécessaire

        #     txt_file_name = input_file_name.replace(".wav", ".txt")
        #     txt_file_path = os.path.join(texts_dir, txt_file_name)

        #     with open(txt_file_path, "w", encoding="utf-8") as f:
        #         f.write(input_str)
        #         f.flush()

        #     response = "..."
        #     output_file_path = self.model.text_to_speech(response)

        #     # Lit le fichier WAV
        #     data, samplerate = sf.read(output_file_path, dtype='int16')

        #     sd.play(data, samplerate)
        #     sd.wait()

    def d(self):
        self.view.display()



