from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from leftbar import Left
from rightbar import Right
from midbar import Mid

from listener import Listener

import sys
app = QtWidgets.QApplication(sys.argv)
app.setApplicationName("DNS Tool")


class Ventana(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ventana, self).__init__(parent)

        self.setStyleSheet("""
            * {
                font-family: proxima-nova;
                font-size: 16pt;
                color: #ffffff;
                background-color: #171717;
            }
                           
            QSplitter:handle {
                background-color: #c0c0c0;
            }
        """)

        # register listeners
        Listener("data")
        Listener("query")
        Listener("complete")
        
        # resize window as width and height div by 2
        primary_screen = app.primaryScreen()
        screen_geometry = primary_screen.geometry()

        w = screen_geometry.width()
        h = screen_geometry.height()

        self.resize(int(w/2), int(h/2))

        # Create layout for main window
        layout = QtWidgets.QHBoxLayout()

        # Create Diedrico widgets
        left = Left()
        mid = Mid()
        right = Right()

        # Set up layout with splitter
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(mid)
        splitter.addWidget(right)
        splitter.setHandleWidth(4)

        layout.addWidget(left, 1)
        layout.addWidget(splitter, 4)
        
        # Set layout as central widget
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        mid.side.clicked.connect(self.toggle)

        self.left = left
        self.mid = mid
        self.right = right

    def toggle(self):
        if self.left.isHidden():
            self.left.show()
            self.mid.side.resetEvent()
        else:
            self.left.hide()
            self.mid.side.pressEvent()


        '''
        # Load styles from external CSS file
        style_file = QtCore.QFile("styles.css")
        if style_file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
            style_sheet = style_file.readAll().data().decode("utf-8")
            self.setStyleSheet(style_sheet)
        '''
            
if __name__ == "__main__":
    ui = Ventana()
    ui.show()
    sys.exit(app.exec_())
