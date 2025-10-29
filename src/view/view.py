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


class View:
    def __init__(self):
        self.btn_is_pressed = False
        self.language = "Nerderlands"

    def get_btn_is_pressed(self): return self.btn_is_pressed

    def get_language(self): return self.language

    # def display(self):
    #     """Affiche l'interface utilisateur."""
    #     # Create a dropdown menu for selecting a hobby
    #     self.language = st.selectbox("Select a language:", ['Nerderlands', 'French', 'English'])

    #     st.title("Voice Reco")

    #     img = Image.open("image/logo.png")
    #     st.image(img, width=200)

    #     if st.button("Record"):
    #         self.btn_is_pressed = True


    def display(self):
        """Affiche une UI soignée pour l'app de reconnaissance vocale."""

        # --- Config page (à appeler une seule fois, au tout début du script idéalement)
        try:
            st.set_page_config(page_title="Voice Reco", page_icon="🎙️", layout="centered")
        except Exception:
            # Streamlit n'aime pas set_page_config quand il est déjà appelé
            pass

        # --- CSS léger
        st.markdown("""
            <style>
            .app-title { 
                font-size: 2.2rem; font-weight: 800; 
                background: linear-gradient(90deg,#4f46e5,#06b6d4);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin-bottom: .2rem;
            }
            .subtle { color: rgba(255,255,255,0.7); font-size: 0.95rem; }
            .card { border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 18px; }
            .muted { color: rgba(255,255,255,0.6); font-size: .9rem; }
            .status-dot { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:8px; }
            </style>
        """, unsafe_allow_html=True)

        # --- État
        if "recording" not in st.session_state:
            st.session_state.recording = False
        if "language" not in st.session_state:
            st.session_state.language = "French"

        # --- Barre latérale
        st.sidebar.header("⚙️ Paramètres")
        self.language = st.sidebar.selectbox(
            "Langue / Language",
            ["French 🇫🇷", "English 🇬🇧", "Nederlands 🇧🇪"],
            index=["French 🇫🇷", "English 🇬🇧", "Nederlands 🇧🇪"].index({
                "French": "French 🇫🇷",
                "English": "English 🇬🇧",
                "Nederlands": "Nederlands 🇧🇪"
            }.get(st.session_state.language, "French 🇫🇷"))
        )
        # garde un simple code langue
        st.session_state.language = (
            "fr-BE" if "French" in self.language
            else "en-GB" if "English" in self.language
            else "nl-BE"
        )

        # --- En-tête
        st.markdown('<div class="app-title">Voice Reco</div>', unsafe_allow_html=True)
        st.caption("🎤 Enregistrez, transcrivez et synthétisez la voix — simple & rapide.")

        # --- Logo centré
        logo_path = Path("image/logo.png")
        if logo_path.exists():
            col_logo = st.columns([1,2,1])[1]
            with col_logo:
                st.image(Image.open(logo_path), width=160)

        # --- Corps
        col_left, col_right = st.columns([1,1])

        with col_left:
            st.markdown("#### 🎙️ Enregistrement")
            with st.container(border=True):
                # statut
                color = "#22c55e" if st.session_state.recording else "#64748b"
                label = "En cours..." if st.session_state.recording else "Prêt"
                st.markdown(
                    f'<span class="status-dot" style="background:{color}"></span>'
                    f'<span class="muted">Statut : {label}</span>',
                    unsafe_allow_html=True
                )

                # bouton toggle
                col_btn1, col_btn2 = st.columns([1,1])
                with col_btn1:
                    if not st.session_state.recording:
                        if st.button("▶️ Commencer l’enregistrement", use_container_width=True, type="primary"):
                            st.session_state.recording = True
                            self.btn_is_pressed = True
                    else:
                        if st.button("⏹️ Arrêter", use_container_width=True):
                            st.session_state.recording = False
                            self.btn_is_pressed = False

                with col_btn2:
                    st.button("🗑️ Réinitialiser", use_container_width=True, help="Effacer le dernier enregistrement")

                st.divider()
                st.markdown(
                    "<div class='muted'>Astuce : parlez clairement et évitez les bruits de fond pour de meilleurs résultats.</div>",
                    unsafe_allow_html=True
                )

        with col_right:
            st.markdown("#### 🧪 Aperçu & Actions")
            with st.container(border=True):
                st.write("• Langue sélectionnée :", f"`{st.session_state.language}`")
                st.write("• Sortie audio :", "`WAV (LINEAR16)`")
                st.write("• Ponctuation automatique :", "`activée côté STT`")
                st.divider()
                st.markdown("##### Actions rapides")
                a1, a2 = st.columns(2)
                with a1:
                    st.button("📝 Transcrire", use_container_width=True)
                with a2:
                    st.button("🗣️ Text → Speech", use_container_width=True)
                st.caption("Les transcriptions seront nettoyées (suppression *** et …) avant TTS.")

        # --- Pied de page
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="subtle">© 2025 • Voice Reco • Made with Streamlit</div>', unsafe_allow_html=True)

