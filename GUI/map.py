from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl  # Import QUrl


class MapWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QWebEngineView widget
        self.webview = QWebEngineView()

        # Create a QUrl object with the URL string
        url = QUrl("https://www.openstreetmap.org")

        # Set the URL using the QUrl object
        self.webview.setUrl(url)

        layout.addWidget(self.webview)