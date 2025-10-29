from model.model import Model

class Controller:
    def __init__(self):
        self.model = Model()

    def handle_record(self):
        """Appelle le modèle pour enregistrer le son."""
        self.model.text_to_speech("bonjour, comment sa va ?") #####
        return self.model.record_audio()
