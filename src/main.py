import streamlit as st
import pandas as pd
import matplotlib as m
import numpy as np
from google.cloud import speech_v2 as speech
from sentence_transformers import SentenceTransformer,util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from controller.controller import Controller
from view.view import View

# app_router.py (exemple d’usage)
from controller.other import load_sheet, build_index_from_sheet, top_k_from_query, chunk_text_by_id

SHEET_PATH = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/detailed_fr_chunks.xlsx"  # ou .csv
x_path = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/detailed_fr_chunks.xlsx"
def load_theme():
    themes = []
    with open("data/themes/themes_fr.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                label, keywords = line.strip().split("|", 1)
                themes.append(label.strip() + " : " + keywords.strip())
    return themes

def load_matching(themes,query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    text_embedding = model.encode(query)
    theme_embeddings = model.encode(themes)
    cos_scores = util.cos_sim(text_embedding, theme_embeddings)[0]

    best_theme_id = cos_scores.argmax()
    best_theme = themes[best_theme_id]
    best_score = cos_scores[best_theme_id]

    return best_theme,best_score

def find_chunk(best_theme):
    return True

def find_relevant_chunks_xlsx(
    xlsx_path: str,
    theme: str,
    sheet_name: str | int | None = 0,   # nom/indice de la feuille (0 = première)
    top_k: int = 5,
    use_embeddings: bool = False,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
):
    """
    xlsx_path    : chemin vers le .xlsx
    theme        : le thème extrait (string)
    sheet_name   : nom/indice de la feuille (None = toutes fusionnées)
    top_k        : nb de résultats
    use_embeddings : True pour Sentence-Transformers (plus lent, plus robuste)
    """
    # 1) Lire le XLSX
    if sheet_name is None:
        # concat toutes les feuilles si None
        xls = pd.read_excel(xlsx_path, sheet_name=None, engine="openpyxl")
        df = pd.concat(xls.values(), ignore_index=True)
    else:
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine="openpyxl")

    # 2) Dernière colonne = texte (selon ta capture)
    text_col = df.columns[-1]
    texts = df[text_col].astype(str).fillna("")

    # 3) Colonne du chunk_name (fallback: 4e colonne comme sur ta capture)
    if "chunk_name" in df.columns:
        chunk_names = df["chunk_name"].astype(str)
        chunk_name_col = "chunk_name"
    else:
        chunk_names = df.iloc[:, 3].astype(str)
        chunk_name_col = df.columns[3]

    # (optionnel) chunk_id si présent
    has_chunk_id = "chunk_id" in df.columns

    # 4) Similarités
    if use_embeddings:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name)
        embeds = model.encode(texts.tolist(), normalize_embeddings=True, show_progress_bar=False)
        q = model.encode([theme], normalize_embeddings=True)[0]
        scores = embeds @ q  # cos sim car normalisés
    else:
        vec = TfidfVectorizer(min_df=1).fit(texts.tolist() + [theme])
        X = vec.transform(texts)
        q = vec.transform([theme])
        scores = cosine_similarity(X, q).ravel()

    # 5) Top-k
    top_idx = np.argsort(-scores)[:top_k]

    # 6) Sortie propre : chunk_id (si dispo), chunk_name, score, aperçu du texte
    cols = []
    if has_chunk_id:
        cols.append("chunk_id")
    cols.append(chunk_name_col)

    out = (
        df.iloc[top_idx]
        .assign(score=scores[top_idx], preview=texts.iloc[top_idx].str.slice(0, 160))
        [cols + ["score", "preview"]]
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )
    return out

def main():
    controller = Controller(View())
    controller.d()
    #controller.load_data()

    query = "enfants mineurs" #request sur le speech to text
    themes = load_theme()
    best_theme, best_score = load_matching(themes,query)

    print(f"Thème détecté : {best_theme} (score : {best_score:.2f})")

    chunk_file = find_chunk(best_theme)
    results = find_relevant_chunks_xlsx(x_path, best_theme, sheet_name=0, top_k=5, use_embeddings=False)
    print(results)

if __name__ == "__main__":
    main()