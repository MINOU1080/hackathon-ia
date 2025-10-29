from asyncio import sleep
import streamlit as st
from model.model import Model
from view.view import View
import pandas as pd
import json
import numpy as np
from sentence_transformers import SentenceTransformer


path_fr = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/similar_fr_chunks.json"
path_eng = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_en_2025_09_23/similar_eng_chunks.json"
path_nl = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_nl_2025_09_23/similar_nl_chunks.json"


class Controller:
    def __init__(self,view):
        self.view = view
        self.model = Model()

    def handle_record(self):
        """Appelle le modèle pour enregistrer le son."""
        self.model.text_to_speech("bonjour, comment sa va ?") #####

        transcript = self.model.speech_to_text("output.mp3")
        st.write("Texte complet :", transcript)

        return self.model.record_audio()

    def d(self):
        self.view.display()

    def load_data(self):
        with open(path_fr, "r", encoding="utf-8") as f:
            similar_data = json.load(f)

            matrix = similar_data.get("matrix", {})
            preview_chunks = similar_data.get("chunks", {})

            print("Nb chunks listés :", len(matrix))
            print("Nb preview chunks :", len(preview_chunks))
            print("preview")
            print(preview_chunks[0])
            """ print("printttt")
            for i, (cid, neigh) in enumerate(matrix.items()):
                print(f"\nChunk: {cid}")
                print("Neighbors:", list(neigh.items()))  # les 3 premiers voisins
            """

