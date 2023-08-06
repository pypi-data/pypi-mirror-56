from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSplitter

from .collection_toc import CollectionTOCView
from .collection_body import CollectionBody


class CollectionContainer(QFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        self._app = app

        self._splitter = QSplitter(self)
        self.collection_toc = CollectionTOCView(self._app, self._splitter)
        self.collection_body = CollectionBody(self._app, self._splitter)

        self._layout = QHBoxLayout(self)

        self._setup_ui()

    def _setup_ui(self):
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._splitter.setHandleWidth(0)
        self._splitter.addWidget(self.collection_toc)
        self._splitter.addWidget(self.collection_body)
        self._layout.addWidget(self._splitter)
