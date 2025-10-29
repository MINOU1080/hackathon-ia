from model.model import Model

class Controller:
    def __init__(self):
        self.model = Model()

    def handle_record(self):
        """Appelle le modèle pour enregistrer le son."""
        return self.model.record_audio()
