import socket
import pickle #for transferring objects via server

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "10.11.4.234"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("nothing")
            pass
    
    # def send_num_of_players(self,number):
    #     try:
    #         self.client.send(str.encode(number))
    #     except socket.error as e:
    #         print(e)

    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*4))
        except socket.error as e:
            print(e)
        
