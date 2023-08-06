from PyQt5.QtWidgets import QFrame, QSizePolicy


class CollectionBody(QFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        self._app = app

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
