from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel

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

        dummy_data = r"""
        Tracing route to dns.google [8.8.8.8]
        over a maximum of 30 hops:

        1      18 ms    18 ms    18 ms  10.8.0.1
        2      54 ms    36 ms    38 ms  185.221.135.65
        3      35 ms    32 ms    32 ms  23.147.224.21
        4      23 ms    21 ms    18 ms  23.147.224.17
        5      23 ms    22 ms    59 ms  [Destination IP]
        6      24 ms    23 ms         *
        7      22 ms    22 ms    31 ms  [Destination IP]
        8      20 ms    22 ms    35 ms  [Destination IP]
        9         *         *         *
        10      24 ms    21 ms    22 ms  [Destination IP]
        11      24 ms    23 ms    24 ms  [Destination IP]
        12      21 ms    22 ms    23 ms  [Destination IP]
        13      23 ms    21 ms    20 ms  dns.google [8.8.8.8]

        Trace complete.
        """

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