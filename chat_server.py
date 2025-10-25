from socket import *
from threading import *

class Chat_Server:
    Clients=[]
    # Create a TCP socket
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen()
        print(f"Chat server started on {self.host}:{self.port}")

    # Listen to connections on main thread. When a connection recieved, create new thread to handle it & add client to list of clients
    def listen(self):
        while True:
            client_Socket,address=self.server_socket.accept()
            print("Connection from "+str(address))
            client_name=client_Socket.recv(1024).decode()
            
            # check for duplicate usernames
            if any(c['client_name'] == client_name for c in Chat_Server.Clients):
                client_Socket.send("Username already exists. Try another name.".encode())
                client_Socket.close()
                continue

            client={'client_name':client_name,'client_socket':client_Socket}
            # broadcast that a new client has connected
            self.broadcast_message(client_name,"\033[1;32;40m"+client_name+" has joined the chat!"+"\033[0m")
            Chat_Server.Clients.append(client)
            Thread(target=self.handle_new_client,args=(client,)).start()

    # Handle new client connecting to the server
    def handle_new_client(self,client):
        client_name=client['client_name']
        client_socket=client['client_socket']
        while True:

            # 1. listen out message of client
            client_message=client_socket.recv(1024).decode()
            if not client_message:
                break

            # 2. client disconnects if he types /quit message
            if client_message.strip() == client_name + ": /quit":
                self.broadcast_message(client_name, f"\033[1;31;40m{client_name} has left the chat!\033[0m")
                Chat_Server.Clients.remove(client)
                client_socket.close()
                break

            # 3. check for private message e.g. @Abdullah mids next week scare me!
            elif "@" in client_message.split(": ", 1)[1]:
                content = client_message.split(": ", 1)[1]
                if content.startswith("@"):
                    parts = content.split(" ", 1)
                    if len(parts) > 1:
                        target_name = parts[0][1:]
                        private_msg = parts[1]
                        self.unicast_message(client_name, target_name, private_msg)
                    else:
                        client_socket.send("Invalid private message format. Use @username message".encode())
                else:
                    self.broadcast_message(client_name, "-> " +client_message)
                    
            # 4. normal broadcast
            else:
                 self.broadcast_message(client_name, "-> "+ client_message)

    # Send msg to every client except sender
    def broadcast_message(self,sender_name,message):
        for client in self.Clients:
            client_name=client['client_name']
            client_socket=client['client_socket']
            # send msg to everyone except the one sending the msg
            if client_name!=sender_name:
                client_socket.send(message.encode())

    # Send private msgs
    def unicast_message(self, sender_name, target_name, message):
        # SAMPLE: Abdullah: @Hammad HELLOOO
        found = False
        for client in self.Clients:
            if client['client_name'] == target_name:
                client['client_socket'].send(f"-> \033[1;34;40m[Private from {sender_name}] {message}\033[0m".encode())
                found = True
                break
        if not found:
            for client in self.Clients:
                if client['client_name'] == sender_name:
                    client['client_socket'].send(f"-> \033[1;31;40mUser {target_name} not found.\033[0m".encode())
                    break

if __name__=="__main__":
    server=Chat_Server('127.0.0.1',12000)
    server.listen()
