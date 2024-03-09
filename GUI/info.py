from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from listener import Listener

class Info(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Info, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.setStyleSheet("""
            QLabel {
                
            }

            QPushButton {
                background-color: #2f2f2f;
                font-size: 12pt;
            }
                           
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 2px;
                font-size: 12px;
            }
        
        """)


        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allows the scroll area to resize its widget

        scroll_area.setStyleSheet(
            """
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0; /* Background color of the scrollbar */
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

   
        label = QLabel("Hops")
        
        # Create a widget to contain the layout
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)

        # Add items to the layout
        for i in range(6):
            layout.addWidget(Ele())  # Assuming Ele() is your custom widget class

        # Set the container widget as the widget of the scroll area
        scroll_area.setWidget(container)

        # Set up layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(label)
        main_layout.addWidget(scroll_area)

        self.layout = layout

        Listener.Get("data").subscribe(self.update)


    def update(self, data):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

        for i in range(6):
            self.layout.addWidget(Ele())
            
        



class Ele(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ele, self).__init__(parent)
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

            QPushButton {
                background-color: #2f2f2f;
                font-size: 12pt;
            }
                           
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 2px;
                font-size: 12px;
            }
        
        """)

        
        self.label1 = QLabel("Hop: 1")
        self.label2 = QLabel("Latency: 2")
        self.label3 = QLabel("DNSSEC: False")
        
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)


        self.setLayout(layout)