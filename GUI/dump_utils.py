"""
files named based on some ctr var
just have the query as the first line in the file
"""

from PyQt5.QtCore import QFileSystemWatcher, QDir
from ip2geotools.databases.noncommercial import DbIpCity

from listener import Listener

import time
import asyncio
import os
import glob
import subprocess
import re

class DumpUtils():
    def __init__(self):
        self.ctr = 0
        self.data = {}
        self.directory = "./Dumps"

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                #os.remove(file_path)
                pass

        Listener.Get("query").subscribe(self.get_new_data)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self.file_added)

        # Set the directory to watch
        directory_to_watch = './Dumps'
        self.file_watcher.addPath(directory_to_watch)
    
    def _parse_hopdump(self, filename):
        hops = []
        with open(filename, "r") as file:
            for line in file:

                # Extracting only the IPs and numbers
                match = re.search(r'(\d+):\d+:\d+\s+(\d+)\s+(.+)$', line, re.MULTILINE)

                if match:
                    second_num = match.group(2)
                    ip_list = match.group(3).split()


                    # get all locations

                    locations = []
                    for i in range(len(ip_list)):
                        ip = ip_list[i]
                        response = DbIpCity.get(ip, api_key='free')
                        locations.append({
                            'lat' : response.latitude,
                            'long' : response.longitude,
                            'city' : response.city,
                            'country' : response.country,
                            'ip' : ip,
                            'num' : str(i)
                        })

                    hops = locations
                    break
                
        return hops
    
    def _parse_raw(self, filenames):
        data = []
        file_string = ""
        for filename in filenames:
            with open(filename, 'r') as file:
                for line in file:
                    file_string += line
                file_string += '\n'
                file_string += '\n'
                file_string += '\n'
        return file_string

    def _parse_dump(self, filename):
        res = []
        latencys = []
        with open(filename, "r") as file:

            # Iterate through each line in the file
            for line in file:
                # Split the line by ':'
                parts = line.strip().split(' ')
  
                # Check if the line contains nameserver DNSSEC enabled information
                if parts[0] == "NAMESERVER:":
                    res.append(line)

                # Check if the line contains domain DNSSEC enabled information
                elif parts[0] == "DOMAIN:":
                    res.append(line)

                elif re.match(r'^\d{2}:\d{2}:\d{2}\t\d+\.\d+$', parts[0]):
                    time_and_value = parts[0].split('\t')  # Split the string by the tab character
                    value = time_and_value[1]  # Get the second part after splitting, which is '28.8'
                    value_as_float = float(value)
                    latencys.append(value_as_float)

                    # only chart 10
                    if len(latencys) > 10:
                        break
        return {
            'latency' : latencys,
            'dnssec' : res
        }


    def file_added(self, path):
        return
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
    

    def get_new_data(self, arg1, arg2=None):
        self.ctr += 1

        # Path to shell script
        script_path = "./main.sh"

        for filename in ['dump.txt', 'hopdump.txt', 'rt.txt']:
            path = os.path.join("./", filename)
            if os.path.isfile(path):
                os.remove(path)

        args = [arg1, arg2] if arg2 else [arg1]

        print(args)

        # Start the subprocess
        subprocess.run([script_path] + args)

        data = {}
        data['dnssec'] = self._parse_dump("./dump.txt")
        data['hops'] = self._parse_hopdump("./hopdump.txt")
        data['raw'] = self._parse_raw(["./dump.txt", "./hopdump.txt"])

        Listener.Get("data").notify(data)

    def _wait_for_file(self, query):
        pass
        
        """
        while not os.path.exists(os.path.join(self.directory, filename)):
            time.sleep(0.5)

        data = None
        with open(path, 'r') as file:
            data = self._parse(file.read())    
        """