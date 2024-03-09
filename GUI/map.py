from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
import io
import pandas as pd

from listener import Listener

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webView = QWebEngineView()
        layout.addWidget(self.webView)

        Listener.Get("data").subscribe(self.create)
        self.empty()

    def empty(self):
        coordinate = (39.8283, -98.5795)
        m = folium.Map(
            title='Stamen Terrain',
            zoom_start=3,
            location=coordinate
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        data.seek(0)

        html = data.getvalue().decode()
        self.webView.setHtml(html)

    def create(self, data=None):
        data = [(40.7128, -74.0060),  # New York City
                (34.0522, -118.2437),  # Los Angeles
                (41.8781, -87.6298),   # Chicago
                (29.7604, -95.3698)]    # Houston
        
        coordinate = (39.8283, -98.5795)
        m = folium.Map(
            title='Stamen Terrain',
            zoom_start=3,
            location=coordinate
        )

        for i in range(len(data)):
            coord = data[i]
            color = 'blue'
            if i == 0:
                color = 'green'
            elif i == len(data)-1:
                color = 'red'
            
            folium.Marker(
                location=coord,
                popup="hey",
                icon=folium.Icon(color=color, icon='none')
            ).add_to(m)

        folium.PolyLine(locations=data, color='blue').add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        data.seek(0)

        html = data.getvalue().decode()

        self.webView.setHtml(html)

