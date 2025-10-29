from http.client import responses
import os

import pandas as pd
import numpy as np
import re
import unicodedata
import time
from sentence_transformers import SentenceTransformer,util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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


from extraction import generate_sql_inserts
from controller.controller import Controller
from controller.auth_controller import AuthController
from view.view import View


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

def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    return s

def fun(path, user_query):
    start_path = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/"
    fullpath = start_path + path
    with open(fullpath, "r", encoding="utf-8") as f:
        text = f.read()

    # Regex plus robuste : '### question' puis réponse jusqu'au prochain '###' en début de ligne
    pattern = r"^###\s*(.+?)\s*\r?\n+([\s\S]*?)(?=^###|\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL | re.MULTILINE)

    faq = []
    for q_text, r_text in matches:  # ✅ éviter d'écraser 'user_query'
        faq.append({
            "question": q_text.strip(),
            "reponse": r_text.strip()
        })

    if not faq:
        return None, 0.0, None

    all_questions = [item["question"] for item in faq]

    unique_list = list(dict.fromkeys(all_questions))

    #print("all question")
    #print(all_questions)

    print("unique ")
    print(unique_list)
    # Normalisation pour robustesse (accents/casse/espaces)
    norm_questions = [_normalize(q) for q in unique_list]
    norm_query = _normalize(user_query)

    vec = TfidfVectorizer().fit(norm_questions + [norm_query])
    q_vec = vec.transform([norm_query])
    faq_vec = vec.transform(norm_questions)

    scores = cosine_similarity(faq_vec, q_vec).ravel()

    best_idx = scores.argmax()
    best_score = float(scores[best_idx])
    best_match = faq[best_idx]

    # Retourne (question, score, réponse)
    return best_match["question"], best_score, best_match["reponse"]

def main():
    controller = Controller(View(),AuthController())

    language = controller.get_view().get_language()
    controller.d()
    generate_sql_inserts()
    controller.handle_record()

    t0 = time.time()
    query = "Est-il facile de passer de mon compte à l’aperçu de mes enfants ?" #request sur le speech to text
    themes = load_theme()
    best_theme, best_score = load_matching(themes,query)

    if controller.get_view().get_btn_is_pressed(): # and controller.is_connected():
        ###############################


        path_input_file, input_file_name = controller.get_model().record_voice()
        query = controller.get_model().speech_to_text(path_input_file)
        # print(query)
        texts_dir = "data/texts"
        os.makedirs(texts_dir, exist_ok=True)  # crée le dossier si nécessaire

        txt_file_name = input_file_name.replace(".wav", ".txt")
        txt_file_path = os.path.join(texts_dir, txt_file_name)

        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(query)
            f.flush()
        
        ###############################

        themes = load_theme()
        best_theme, best_score = load_matching(themes,query)

        print(f"Thème détecté : {best_theme} (score : {best_score:.2f})")

        chunk_file = find_chunk(best_theme)
        res = find_relevant_chunks_xlsx(x_path, best_theme, sheet_name=0, top_k=5, use_embeddings=False)
        print(res)

        chunk_names = res["chunk_name"].tolist()   # top-k chunks
        print(chunk_names)

        # 🔎 Parcourt tous les chunks et garde le meilleur match global
        best_global = {
            "chunk": None,
            "question": None,
            "reponse": None,
            "score": 0.0
        }

        for fname in chunk_names:
            best_q, score, ans = fun(fname, query)
            if score is None:
                continue
            if score > best_global["score"]:
                best_global.update({
                    "chunk": fname,
                    "question": best_q,
                    "reponse": ans,
                    "score": score
                })

        elapsed = time.time() - t0
        print(f"⏱️ Temps total match des Q/R : {elapsed:.3f} sec")

        # Résultat final
        if best_global["score"] == 0.0:
            reponse = None
        else:
            reponse = best_global["reponse"]

        print("✅ Best chunk:", best_global["chunk"])
        print("🔍 Best question:", best_global["question"])
        print("⭐ Score:", best_global["score"])
        print("🧾 Réponse:", reponse) ## response

        output_file_path = controller.get_model().text_to_speech(reponse)

        # Lit le fichier WAV
        data, samplerate = sf.read(output_file_path, dtype='int16')

        sd.play(data, samplerate)
        sd.wait()

    # elif not controller.is_connected():
    #     name = controller.get_view().get_name()
    #     birthdate = controller.get_view().get_birthdate()
    #     print("name")
    #     print(name)
    #     print(birthdate)

    #     controller.send_query(name,birthdate)



if __name__ == "__main__":
    main()