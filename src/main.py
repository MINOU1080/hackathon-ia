
import re
import unicodedata
import time
from sentence_transformers import SentenceTransformer,util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd
import sounddevice as sd
import soundfile as sf
import numpy as np
from sentence_transformers import SentenceTransformer


from extraction import generate_sql_inserts
from controller.controller import Controller
from controller.auth_controller import AuthController
from view.view import View

x_path = "data/10. Hackathon_Leuven_2025/chunks/500_750_processed_be_fr_2025_09_23/detailed_fr_chunks.xlsx"


def main():
    controller = Controller(View(),AuthController())

    language = controller.get_view().get_language()
    controller.d()
    generate_sql_inserts()

    t0 = time.time()

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
        themes = controller.load_theme()
        best_theme, best_score = controller.load_matching(themes,query)

        print(f"Thème détecté : {best_theme} (score : {best_score:.2f})")

        chunk_file = controller.find_chunk(best_theme)
        res = controller.find_relevant_chunks_xlsx(x_path, best_theme, sheet_name=0, top_k=5, use_embeddings=False)

        chunk_names = res["chunk_name"].tolist()   # top-k chunks

        best_global = {
            "chunk": None,
            "question": None,
            "reponse": None,
            "score": 0.0
        }

        for fname in chunk_names:
            best_q, score, ans = controller.fun(fname, query)
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

        data, samplerate = sf.read(output_file_path, dtype='int16')

        sd.play(data, samplerate)
        sd.wait()

if __name__ == "__main__":
    main()