# listens for new dump file, then passes it to the parser

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QFileSystemWatcher, QDir
import sys

class FileWatcherDemo(QMainWindow):
    def __init__(self):
        super(FileWatcherDemo, self).__init__()

        self.setWindowTitle("File Watcher Demo")

        # Set up UI
        self.central_widget = QLabel("No file added yet.")
        self.setCentralWidget(self.central_widget)

        self.add_file_button = QPushButton("Add File")
        self.add_file_button.clicked.connect(self.add_file)
        self.status_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.add_file_button)
        layout.addWidget(self.status_label)
        self.central_widget.setLayout(layout)

        # Set up file watcher
        self.directory_to_watch = QDir.currentPath()  # You can replace this with the desired directory
        self.file_watcher = QFileSystemWatcher([self.directory_to_watch], self)
        self.file_watcher.fileChanged.connect(self.file_added)

    def add_file(self):
        # Simulate adding a file to the directory
        new_file_path = QDir(self.directory_to_watch).filePath("new_file.txt")
        with open(new_file_path, 'w') as file:
            file.write("Hello, this is a new file!")

        self.status_label.setText(f"File added: {new_file_path}")

    def file_added(self, path):
        self.status_label.setText(f"File added: {path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = FileWatcherDemo()
    demo.show()
    sys.exit(app.exec_())
