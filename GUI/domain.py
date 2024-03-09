from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5.QtCore import QSize

from listener import Listener

class IconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setFixedSize(30,30)

        self.activeIcon = QIcon("./GUI/select.png")
        self.inactiveIcon = QIcon("./GUI/select-inactive.png")
        self.setIcon(self.activeIcon)
        self.setIconSize(QSize(25,25))
        
        self.setStyleSheet("""          
            QPushButton {
                background-color: #171717;
                padding: 0px;
                outline: none;
                border: none;
            }
        """)

    def pressEvent(self):
        self.setIcon(self.inactiveIcon)

    def resetEvent(self):
        self.setIcon(self.activeIcon)

class BorderedWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.active = True

        Listener.Get("data").subscribe(self.ready_again)
        
        # Set the frame style to include a border
        self.setFrameStyle(QFrame.Box | QFrame.Plain)

        # Create a layout to arrange child widgets within the frame
        layout = QHBoxLayout(self)
        
        self.text_input = QLineEdit()
        self.button = IconButton()

        # Connect the returnPressed signal to the on_enter_pressed method
        self.text_input.returnPressed.connect(self.activated)
        self.button.clicked.connect(self.activated)

        # Add child widgets to the layout
        layout.addWidget(self.text_input)
        layout.addWidget(self.button)

        self.setStyleSheet("""
            QFrame {
                background-color: #171717;
                border-radius: 8px;
                border: 2px solid #2f2f2f;
                padding: 0px;
            }
             
            QLineEdit {
                font-size: 12px;
                border: none;
                padding: 0px;
            }
        """)

    def activated(self):
        if not self.active:
            return
        
        self.active = False

        if self.text_input.text().strip() == "":
            return

        self.button.pressEvent()
        Listener.Get("query").notify(self.text_input.text().strip())
        self.text_input.clear()

    def ready_again(self, data):
        print("here")
        self.active = True
        self.button.resetEvent()

class DomainInput(QFrame):
    def __init__(self, parent=None):
        super(DomainInput, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.setStyleSheet("""
            QLabel {
                padding-bottom: 10px;
            }
        """)

        # Create widgets
        self.label = QLabel("Enter Domain/IP")
        self.inputWidget = BorderedWidget()
        
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.inputWidget)
        layout.addStretch(1)  # Add some vertical stretch
        self.setLayout(layout)

        