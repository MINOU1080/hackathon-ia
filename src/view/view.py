# import streamlit as st
# from PIL import Image
# import io
# import os
# from datetime import datetime
# import sounddevice as sd
# import soundfile as sf
# import streamlit as st
# from PIL import Image
# from pathlib import Path
# from datetime import date  # <-- ajoute ceci



# class View:
#     def __init__(self):
#         self.btn_is_pressed = False
#         self.language = "Nerderlands"
#         self.name = ""
#         self.birthdate = " "

#     def get_btn_is_pressed(self): return self.btn_is_pressed

#     def get_language(self): return self.language

#     def get_name(self):
#         return self.name

#     def get_birthdate(self):
#         return self.birthdate
    

#     def display(self):
#         """Affiche l'interface utilisateur."""
#         st.title("Voice Reco")

#         img = Image.open("image/logo.png")
#         st.image(img, width=200)

#         st.sidebar.header("⚙️ Paramètres")
#         self.language = st.sidebar.selectbox(
#             "Language",  # <-- label obligatoire
#             ["French", "English", "Nederlands"]
#         )

#         st.subheader("Login")
#         self.name = st.text_input("Your name", value=self.name or "")
#         self.birthdate = st.date_input(
#             "Birthdate",
#             value=self.birthdate or date(2000, 1, 1),
#             min_value=date(1900, 1, 1),
#             max_value=date.today()
#         )

#         if st.button("Record"):
#             self.btn_is_pressed = True

from datetime import date, datetime
from pathlib import Path
from PIL import Image
import streamlit as st

def _safe_date(v, fallback=date(2000, 1, 1)):
    if v is None:
        return fallback
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, str):
        if v.lower() == "today":
            return date.today()
        try:
            return date.fromisoformat(v)  # "YYYY-MM-DD"
        except ValueError:
            return fallback
    return fallback

class View:
    def __init__(self):
        self.btn_is_pressed = False
        self.name = ""
        self.birthdate = None  # peut être str/date/datetime/None
        self.language = "Nederlands"

    def get_btn_is_pressed(self):
        return self.btn_is_pressed

    def get_btn_is_pressed(self): return self.btn_is_pressed

    def get_language(self): return self.language

    def get_name(self):
        return self.name

    def get_birthdate(self):
        return self.birthdate

    def display(self):
        st.title("Voice Reco")

        logo = Path("image/logo.png")
        if logo.exists():
            st.image(Image.open(logo), width=200)

        if st.button("Record"):
            self.btn_is_pressed = True

        st.sidebar.header("⚙️ Paramètres")
        self.language = st.sidebar.selectbox("Language", ["French", "English", "Nederlands"])

        # --- Login (inputs + bouton 'Login' qui assigne aux attributs)
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=False):
            name_in = st.text_input("Your name", value=self.name or "")
            bdate_in = st.date_input(
                "Birthdate",
                value=(self.birthdate or date(2000, 1, 1)),
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
            do_login = st.form_submit_button("Login")  # <-- bouton

        # if do_login:
        #     self.name = name_in.strip()
        #     self.birthdate = bdate_in
        #     st.success(f"Logged in as {self.name} · {self.birthdate.isoformat()}")
