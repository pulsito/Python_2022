from pydoc import cli
import socket, re
from xmlrpc import client

class Server:
    UDP_MAX_SIZE = 1024
    members = dict()

    def __init__(self, path_to_filter_file):
        with open(path_to_filter_file,'r', encoding='utf-8') as file:
                    self.filter_list = file.read().split("\n")
        
        
    def create_socket(self, host : str = "127.0.0.1", port: int = 3000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host,port))
        print(f"Listening at {host}:{port}")

    def send_to_members(self, msg, client_id):
        for member in self.members.keys():
                if(member!= client_id):
                    self.sock.sendto(msg.encode('utf-8'),member)
    def listen(self):
               
        while True:
            msg, addr = self.sock.recvfrom(self.UDP_MAX_SIZE)
            # print(msg.decode())
            client_id = addr
            msg = msg.decode('utf-8')
            if(addr not in self.members):
                text = msg.split(" ")
                if(text[0] == "/join" and len(text)>1):
                    msg = f'{text[1]} has joined to chat'
                    print(msg)
                    self.send_to_members(msg,client_id)
                    self.members[addr] = text[1]   #add name of member by port
                else:
                    self.sock.sendto("Use command '\join (name)'".encode('utf-8'), addr)
                    print(f"{addr[1]} isn't in chat")
                continue

                
            for word in self.filter_list:
                msg = re.sub(f'(?i){word}(?=\W)', "***", msg)
            msg = f'{self.members[client_id]}: {msg}'
            print(msg)
            self.send_to_members(msg,client_id)
            
        
    

  

if __name__ == "__main__" :
    server = Server("filter.txt")
    server.create_socket()
    server.listen()



