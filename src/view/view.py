import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import streamlit as st
from PIL import Image
from pathlib import Path
from datetime import date  # <-- ajoute ceci



class View:
    def __init__(self):
        self.btn_is_pressed = False
        self.language = "Nerderlands"
        self.name = ""
        self.birthdate = " "

    def get_btn_is_pressed(self): return self.btn_is_pressed

    def get_language(self): return self.language

    def get_name(self):
        return self.name

    def get_birthdate(self):
        return self.birthdate

    def display(self):
        """Affiche une UI soignée multilingue avec login (nom + date de naissance)."""

        # --- Config page
        try:
            st.set_page_config(page_title="Voice Reco", page_icon="🎙️", layout="centered")
        except Exception:
            pass

        # --- CSS léger
        st.markdown("""
            <style>
            .app-title{
                font-size:2.2rem;font-weight:800;
                background:linear-gradient(90deg,#4f46e5,#06b6d4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                margin-bottom:.2rem;
            }
            .subtle{color:rgba(255,255,255,0.7);font-size:.95rem;}
            .muted{color:rgba(255,255,255,0.6);font-size:.9rem;}
            .status-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:8px;}
            </style>
        """, unsafe_allow_html=True)

        # --- État
        st.session_state.setdefault("recording", False)
        st.session_state.setdefault("user", {"name": "", "birthdate": None})

        # --- i18n dictionnaire
        TR = {
            "fr": {
                "sidebar_header": "⚙️ Paramètres",
                "language_label": "Langue / Language",
                "app_title": "Voice Reco",
                "caption": "🎤 Enregistrez, transcrivez et synthétisez la voix — simple & rapide.",
                "record_section": "🎙️ Enregistrement",
                "status_ready": "Prêt",
                "status_recording": "En cours…",
                "start_rec": "▶️ Commencer l’enregistrement",
                "stop": "⛔ Arrêter",
                "reset": "🗑️ Réinitialiser",
                "reset_help": "Effacer le dernier enregistrement",
                "tip": "Astuce : parlez clairement et évitez les bruits de fond pour de meilleurs résultats.",
                "preview_actions": "🧪 Aperçu & Actions",
                "sel_lang": "• Langue sélectionnée :",
                "output": "• Sortie audio :",
                "punct": "• Ponctuation automatique :",
                "enabled": "activée côté STT",
                "actions_header": "Actions rapides",
                "transcribe": "📝 Transcrire",
                "tts": "🗣️ Texte → Parole",
                "clean_note": "Les transcriptions seront nettoyées (suppression *** et …) avant TTS.",
                "login_title": "🔐 Connexion",
                "name": "Votre nom",
                "bdate": "Date de naissance",
                "login_btn": "Se connecter",
                "login_ok": "Bienvenue",
                "connected_as": "Connecté en tant que",
                "footer": "© 2025 • Voice Reco • Made with Streamlit",
            },
            "en": {
                "sidebar_header": "⚙️ Settings",
                "language_label": "Language",
                "app_title": "Voice Reco",
                "caption": "🎤 Record, transcribe and synthesize speech — simple & fast.",
                "record_section": "🎙️ Recording",
                "status_ready": "Ready",
                "status_recording": "Recording…",
                "start_rec": "▶️ Start recording",
                "stop": "⛔ Stop",
                "reset": "🗑️ Reset",
                "reset_help": "Clear the last recording",
                "tip": "Tip: speak clearly and avoid background noise for best results.",
                "preview_actions": "🧪 Preview & Actions",
                "sel_lang": "• Selected language:",
                "output": "• Output audio:",
                "punct": "• Automatic punctuation:",
                "enabled": "enabled in STT",
                "actions_header": "Quick actions",
                "transcribe": "📝 Transcribe",
                "tts": "🗣️ Text → Speech",
                "clean_note": "Transcripts are cleaned (remove *** and …) before TTS.",
                "login_title": "🔐 Login",
                "name": "Your name",
                "bdate": "Birthdate",
                "login_btn": "Sign in",
                "login_ok": "Welcome",
                "connected_as": "Signed in as",
                "footer": "© 2025 • Voice Reco • Made with Streamlit",
            },
            "nl": {
                "sidebar_header": "⚙️ Instellingen",
                "language_label": "Taal",
                "app_title": "Voice Reco",
                "caption": "🎤 Neem op, transcribeer en synthesizeer — eenvoudig en snel.",
                "record_section": "🎙️ Opname",
                "status_ready": "Klaar",
                "status_recording": "Bezig…",
                "start_rec": "▶️ Opname starten",
                "stop": "⛔ Stoppen",
                "reset": "🗑️ Reset",
                "reset_help": "Laatste opname wissen",
                "tip": "Tip: spreek duidelijk en vermijd achtergrondgeluid voor betere resultaten.",
                "preview_actions": "🧪 Voorbeeld & Acties",
                "sel_lang": "• Geselecteerde taal:",
                "output": "• Audio-uitvoer:",
                "punct": "• Automatische interpunctie:",
                "enabled": "ingeschakeld in STT",
                "actions_header": "Snelle acties",
                "transcribe": "📝 Transcriberen",
                "tts": "🗣️ Tekst → Spraak",
                "clean_note": "Transcripten worden opgeschoond (*** en … verwijderd) vóór TTS.",
                "login_title": "🔐 Inloggen",
                "name": "Uw naam",
                "bdate": "Geboortedatum",
                "login_btn": "Inloggen",
                "login_ok": "Welkom",
                "connected_as": "Ingelogd als",
                "footer": "© 2025 • Voice Reco • Gemaakt met Streamlit",
            },
        }

        # --- Barre latérale (langue)
        st.sidebar.header("⚙️ Paramètres")
        lang_choice = st.sidebar.selectbox(
            "Langue / Language",
            ["French 🇫🇷", "English 🇬🇧", "Nederlands 🇧🇪"],
            index=0 if st.session_state.get("lang_key","fr")=="fr"
                else 1 if st.session_state.get("lang_key")=="en"
                else 2
        )

        # Map UI → codes
        if "French" in lang_choice:
            lang_key = "fr"; st.session_state.language = "fr-BE"
        elif "English" in lang_choice:
            lang_key = "en"; st.session_state.language = "en-GB"
        else:
            lang_key = "nl"; st.session_state.language = "nl-BE"
        st.session_state.lang_key = lang_key
        _ = TR[lang_key]  # alias traductions

        # Remplace header sidebar par la traduction
        st.sidebar.header(_["sidebar_header"])
        st.sidebar.markdown(f"**{_['language_label']}**: `{st.session_state.language}`")

        # --- En-tête
        st.markdown(f'<div class="app-title">{_["app_title"]}</div>', unsafe_allow_html=True)
        st.caption(_["caption"])

        # --- Logo centré
        logo_path = Path("image/logo.png")
        if logo_path.exists():
            col_logo = st.columns([1,2,1])[1]
            with col_logo:
                st.image(Image.open(logo_path), width=160)

        # --- Corps
        col_left, col_right = st.columns([1,1])

        # Gauche : Enregistrement
        with col_left:
            st.markdown(f"#### {_['record_section']}")
            with st.container(border=True):
                color = "#22c55e" if st.session_state.recording else "#64748b"
                label = _["status_recording"] if st.session_state.recording else _["status_ready"]
                st.markdown(
                    f'<span class="status-dot" style="background:{color}"></span>'
                    f'<span class="muted">{"Statut" if lang_key=="fr" else "Status" if lang_key=="en" else "Status"} : {label}</span>',
                    unsafe_allow_html=True
                )

                col_btn1, col_btn2 = st.columns([1,1])
                with col_btn1:
                    if not st.session_state.recording:
                        if st.button(_["start_rec"], use_container_width=True, type="primary"):
                            st.session_state.recording = True
                            self.btn_is_pressed = True
                    else:
                        if st.button(_["stop"], use_container_width=True):
                            st.session_state.recording = False
                            self.btn_is_pressed = False

                with col_btn2:
                    st.button(_["reset"], use_container_width=True, help=_["reset_help"])

                st.divider()
                st.markdown(f"<div class='muted'>{_['tip']}</div>", unsafe_allow_html=True)

        # Droite : Login + Actions
        with col_right:
            # --- Login
            st.markdown(f"#### {_['login_title']}")
            with st.form("login_form", clear_on_submit=False, border=True):
                self.name = st.text_input(_["name"], value=st.session_state["user"]["name"] or "")
                bdate_default = st.session_state["user"]["birthdate"] or date(2000,1,1)
                self.birthdate = st.date_input(_["bdate"], value=bdate_default, min_value=date(1900,1,1), max_value=date.today())
                submitted = st.form_submit_button(_["login_btn"])
            if submitted:
                errs = []
                if not name.strip():
                    errs.append({"fr":"Le nom est requis.","en":"Name is required.","nl":"Naam is vereist."}[lang_key])
                if bdate > date.today():
                    errs.append({"fr":"La date ne peut pas être dans le futur.",
                                "en":"Birthdate cannot be in the future.",
                                "nl":"Geboortedatum kan niet in de toekomst liggen."}[lang_key])
                if errs:
                    for e in errs: st.error(e)
                else:
                    st.session_state["user"] = {"name": name.strip(), "birthdate": bdate}
                    st.success(f"{_['login_ok']}, {name.strip()}!")
            if st.session_state["user"]["name"]:
                who = st.session_state['user']['name']
                st.info(f"{_['connected_as']} **{who}**")

            st.markdown("#### " + _["preview_actions"])
            with st.container(border=True):
                st.write(_["sel_lang"], f"`{st.session_state.language}`")
                st.write(_["output"], "`WAV (LINEAR16)`")
                st.write(_["punct"], f"`{_['enabled']}`")
                st.divider()
                st.markdown("##### " + _["actions_header"])
                a1, a2 = st.columns(2)
                with a1:
                    st.button(_["transcribe"], use_container_width=True)
                with a2:
                    st.button(_["tts"], use_container_width=True)
                st.caption(_["clean_note"])

        # --- Pied de page
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="subtle">{_["footer"]}</div>', unsafe_allow_html=True)


