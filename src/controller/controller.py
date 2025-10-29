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

    def handle_record(self):
    #     """Appelle le modèle pour enregistrer le son."""
    #     # self.model.text_to_speech("bonjour, comment sa va ?") #####

    #     # transcript = self.model.speech_to_text("output.mp3")
    #     # st.write("Texte complet :", transcript)
    #     input_audio = self.model.record_audio()
        if self.view.get_btn_is_pressed():
            path_input_file, input_file_name = self.model.record_voice()  
            input_str = self.model.speech_to_text(path_input_file)
            
            texts_dir = "data/texts"
            os.makedirs(texts_dir, exist_ok=True)  # crée le dossier si nécessaire

            txt_file_name = input_file_name.replace(".wav", ".txt")
            txt_file_path = os.path.join(texts_dir, txt_file_name)

            with open(txt_file_path, "w", encoding="utf-8") as f:
                f.write(input_str)
                f.flush()

            response = "Comptes courants | compte à vue, IBAN, RIB, relevé d'identité bancaire, ouverture de compte Cartes & codes | carte bancaire, Maestro, Debit, Visa, Mastercard, CVC, CVV, code PIN, renouvellement Paiements | paiement, sans contact, QR, virement instantané, standing order, domiciliation Virements & transferts | virement SEPA, international, swift, frais, délais Retraits & limites | distributeur, ATM, plafond, limite de paiement, cash À l’étranger | payer à l’étranger, frais, taux de change, voyage Épargne | compte épargne, livret, intérêts, objectifs, Save Up Jeunes & mineurs | compte mineur, autorisation parentale, contrôle parental, Kids/Teens , enfants Investissements | fonds, ETF, titres, profil de risque, ING Invest Prêts & crédits | crédit conso, prêt perso, hypothèque, simulation Assurances | assurance compte, carte, voyage, achats, fraude Sécurité & fraude | phishing, smishing, blocage carte, vol, opposition, authentification forte Banque en ligne | Home’Bank, app ING, login, mot de passe, itsme, authentification Données & confidentialité | données personnelles, RGPD, consulter, modifier, effacer Identité & documents | KYC, vérification, pièce d’identité, justificatif, attestation Attestations & fiscalité | attestation fiscale, impôts, relevés, documents fiscaux Litiges & chargeback | contestation, transaction inconnue, rétrofacturation, différend commerçant Frais & tarifs | commissions, coûts, conditions, grille tarifaire Notifications & alertes | sms, e-mail, push, paramètre d’alerte Service client | contact, support, rendez-vous, agence Problèmes techniques | bug, erreur, connexion, mise à jour, compatibilité Accessibilité | handicap, assistance, fonctionnalités, support dédié Entreprises | compte pro, terminaux de paiement, facturation, SEPA entreprise" # - AI response, ici faire l appel
            output_file_path = self.model.text_to_speech(response)

            # Lit le fichier WAV
            data, samplerate = sf.read(output_file_path, dtype='int16')

            sd.play(data, samplerate)
            sd.wait()

    def d(self):
        self.view.display()



