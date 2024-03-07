from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout

class General(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(General, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.setStyleSheet("""
            QWidget {
                border: 2px solid gray;
            }
                           
            QLabel {
                border: 0px;
            }
        """)

        
        self.label1 = QLabel("Total Latency: 100")
        self.label3 = QLabel("DNSSEC %: 30%")
        
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label3)


        self.setLayout(layout)