from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtGui import QCursor

from listener import Listener

class History(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(History, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.setStyleSheet("""
            QPushButton {
                background-color: #2f2f2f;
                font-size: 12pt;
            }
        """)

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allows the scroll area to resize its widget

        scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background: none;
            }

            QScrollBar:vertical {
                border: none;
                background: transparent; /* Background color of the scrollbar */
                width: 10px; /* Width of the scrollbar */
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #606060; /* Color of the scrollbar handle */
                min-height: 20px; /* Minimum height of the scrollbar handle */
                border-radius: 5px; /* Border radius of the scrollbar handle */
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            """
        )

        # Create a widget to contain the layout
        container = QtWidgets.QWidget()

        layout = QVBoxLayout(container)
        layout.addStretch(0)

        for i in range(5):
            layout.insertWidget(0, HistoryButton("google.com"))
        
        scroll_area.setWidget(container)

        # Set up layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.layout = layout

        Listener.Get("query").subscribe(self.addElement)
        

    def addElement(self, text):
        self.layout.insertWidget(0, HistoryButton(text))



class HistoryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        
        # Set the default style
        self.setStyleSheet('''
            QPushButton {
                background-color: #171717;
                font-size: 12pt;
                border-radius: 5px;
                text-align: left;
                padding: 10px;
            }
            
            QPushButton:hover {
                background-color: #2f2f2f;
            }
            
            QPushButton:pressed {
                background-color: #2f2f2f;
            }
        ''')

        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))


    def mousePressEvent(self, event):
        self.callback(self.text)

