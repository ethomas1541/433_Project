from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from listener import Listener

class Raw(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Raw, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.setStyleSheet("""
            QWidget {
                
            }
                           
            QLabel {
                font-family: "Courier New", monospace;
                font-size: 12px;
                color: #FFFFFF;
                background-color: #000000;
            }
        """)

        dummy_data = ""
        self.label1 = QtWidgets.QLabel(dummy_data + dummy_data)
        self.label1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Set up scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label1)
        
        # Set up layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        Listener.Get("data").subscribe(self.create)

    def create(self, data):
        raw = data['raw']
        self.label1.setText(raw)
        