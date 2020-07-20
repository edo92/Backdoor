import json 
import base64

class Util:
    @staticmethod
    def write_file(path, content):
        with open (path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successfule"
   
    @staticmethod
    def read_file(path):
        print('python code is runing')
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()
            
    @staticmethod
    def utilize_send(conn, data):
        json_data = json.dumps(data)
        conn.send(json_data.encode())
    
    @staticmethod
    def utilize_receive(conn):
        json_data = b""
        while True:
            try:
                json_data = json_data + conn.recv(1024)
                return  json.loads(json_data)

            except ValueError:
                continue