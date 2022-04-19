import socket, threading, os

class Client:
    UDP_MAX_SIZE=1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self):
        while True:
            msg = self.sock.recv(self.UDP_MAX_SIZE)
            print('\r\r' + msg.decode('utf-8') + '\n' + f'you: ', end='')

    def send(self):
        while True:
            msg = input(f'you: ')
            self.sock.send(msg.encode('utf-8'))


    def connect(self, host = "127.0.0.1", port = 3000):
        
        self.sock.connect((host,port))

        threading.Thread(target=self.listen, daemon=True).start()

        os.system('cls')
        print("Welcome to Consolegram")
        name = input("Enter your name: " )
        self.sock.send(f"/join {name}".encode())
        os.system('cls')
        print(f"Welcome to chatroom, {name}!")
        self.send()
       
    
 
client = Client()  
client.connect()