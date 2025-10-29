import streamlit as st
import pandas as pd
import matplotlib as m
import numpy as n
from google.cloud import speech_v2 as speech

from controller.controller import Controller
from view.view import View

# app_router.py (exemple d’usage)
from controller.other import load_sheet, build_index_from_sheet, top_k_from_query, chunk_text_by_id

SHEET_PATH = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/detailed_fr_chunks.xlsx"  # ou .csv



def main():
    controller = Controller(View())

    controller.d()
    controller.load_data()

    df = load_sheet(SHEET_PATH)
    idx = build_index_from_sheet(df)  # => construit les embeddings une seule fois

    # 2) Pour chaque requête (texte venant de ton speech-to-text)
    query = "Comment construire un plan d'épargne ?"
    top = top_k_from_query(idx, query, k=3)

    # top est une liste [(chunk_id, title, score, url), ...]
    best_id, best_title, _, best_url = top[0]
    best_text = chunk_text_by_id(idx, best_id)

    print("REDIRECT:", best_title, best_url)
    print("CONTEXT:", best_text[:500])

if __name__ == "__main__":
    main()