from PyQt5 import QtCore, QtGui, QtWidgets

from node import Square

class NodeGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeGraph, self).__init__(parent)
        self.resize(400, 400)
        self.offset = QtCore.QPoint(0, 0)
        self.scale_factor = 1.0
        self.setAttribute(QtCore.Qt.WA_StyledBackground)  
        self.setStyleSheet("""
            background-color: #212121;
        """)

    """
    Commented until zoom bug fixed

    def wheelEvent(self, event):
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 0.8

        # Update the scale factor
        self.scale_factor *= zoom_factor

        # Ensure the scale factor stays within bounds
        self.scale_factor = max(0.1, min(self.scale_factor, 10.0))

        self.update()
    """
        

    def addNode(self):

        # Calculate the position for the first square to be in the middle of the window
        window_width = self.width()
        window_height = self.height()
        square_size = 100  # Assume square size

        square1_x = int((window_width - square_size) / 2)
        square1_y = int((window_height - square_size) / 2)

        # Create the first square and set its position
        self.square1 = Square(self)  # Red square
        self.square1.scale_factor = self.scale_factor
        self.square1.move(square1_x, square1_y)

        # Position the second square to the right of the first square
        square2_x = square1_x + (square_size*2)  # Position it to the right
        square2_y = square1_y  # Align vertically with the first square

        # Create the second square and set its position
        self.square2 = Square(self)  # Blue square
        self.square2.offset = self.offset
        self.square2.scale_factor = self.scale_factor
        self.square2.move(square2_x, square2_y)

    def enterEvent(self, event):
        print("Enter")

    def leaveEvent(self, event):
        print("Leave")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.RightButton:
            delta = event.pos() - self.last_pos
            self.offset += delta
            self.last_pos = event.pos()
            self.square1.move(self.last_pos.x(), self.last_pos.y())
            self.square2.move(self.last_pos.x(), self.last_pos.y())
            self.update()
