from socket import *
from threading import *
import os

class Chat_Client:
    # Create client, connect to server, ask username and start communication
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.client_socket=socket()
        self.client_socket.connect((self.host,self.port))
        self.name=input("Enter your name: ")
        self.talk_to_server()

    # First send username to server, then start listening for msgs on seperate thread while msg sending are on main thread
    def talk_to_server(self):
        self.client_socket.send(self.name.encode())
        Thread(target=self.recieve_message).start()
        self.send_message()

    # Get user input & send msg to server
    def send_message(self):
        while True:
            client_input=input()
            client_message=self.name+": "+client_input
            self.client_socket.send(client_message.encode())
    
    # Constantly listen to msgs from server & display
    def recieve_message(self):
        while True:
            server_message=self.client_socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)
            print(server_message)

if __name__=="__main__":
    Chat_Client('127.0.0.1',12000)