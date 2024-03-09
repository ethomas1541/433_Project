"""
files named based on some ctr var
just have the query as the first line in the file
"""

from PyQt5.QtCore import QFileSystemWatcher, QDir

from listener import Listener

import time
import asyncio
import os
import glob
import subprocess

class DumpUtils():
    def __init__(self):
        self.ctr = 0
        self.data = {}
        self.directory = "./Dumps"

        Listener.Get("query").subscribe(self.get_new_data)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self.file_added)

        # Set the directory to watch
        directory_to_watch = './Dumps'
        self.file_watcher.addPath(directory_to_watch)

    def file_added(self, path):
        print("detected file")
        list_of_files = glob.glob(os.path.join(path, '*'))
        latest_file = max(list_of_files, key=os.path.getctime)
        
        data = self._parse()
        Listener.Get("data").notify(data)


    def addData(self, filename, data):
        self.data[filename] = data

    def removeData(self, filename):
        del self.data[filename]

    def getData(self, filename):
        return self._parse(filename)

    def _parse(self, input=""):
        return [
            {
                "latency": 20,
                "location": "Oregon",
                "DNSSEC": False
            },

            {
                "latency": 20,
                "location": "Oregon",
                "DNSSEC": False
            },

            {
                "latency": 20,
                "location": "Oregon",
                "DNSSEC": False
            },

            {
                "latency": 20,
                "location": "Oregon",
                "DNSSEC": False
            },
        ]
    
    async def run_shell_script(self):
        shell_script_path = "./testfile.sh"
        await asyncio.create_subprocess_shell(
            f"bash {shell_script_path} {self.ctr}"
        )

    def get_new_data(self, query):
        self.ctr += 1
        asyncio.run(self.run_shell_script())

    def _wait_for_file(self, query):
        pass
        
        """
        while not os.path.exists(os.path.join(self.directory, filename)):
            time.sleep(0.5)

        data = None
        with open(path, 'r') as file:
            data = self._parse(file.read())    
        """