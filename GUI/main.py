from PyQt5 import QtWidgets

from leftbar import Left
from rightbar import Right
from node_graph import NodeGraph

import sys
app = QtWidgets.QApplication(sys.argv)
app.setApplicationName("CS 433 Project")

class Ventana(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ventana, self).__init__(parent)

        """
        # Set background color for the entire widget
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor("#1b1b23"))
        self.setPalette(p)
        """

        self.setStyleSheet("""
            * {
                font-family: proxima-nova;
                font-size: 16pt;
                color: #ffffff;
                background-color: #171717;
            }
        
        """)
        
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
        node_graph = NodeGraph()
        right = Right()

        # Add Diedrico widgets to layout
        layout.addWidget(left, 1)
        layout.addWidget(node_graph, 2)
        layout.addWidget(right, 2)
 
        # Set layout as central widget
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        node_graph.addNode()

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
