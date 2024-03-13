import socket as s
import select as sel
import sys

HOST = ''
PORT = 9876
SOCKET_LIST = []
RECEIVE_BUFF = 4096
#MESSAGE_BUFF = {}  # Store incomplete messages for each client

def chat_server():
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)
    SOCKET_LIST.append(server_socket)

    print("Hi welcome to my private chat, listening on port " + str(PORT) + "...")

    while True:
        #Blocking the flow for new Incomming Connection....
        ready_read, read_write, error = sel.select(SOCKET_LIST, [], [], 0)
        #Waiting for my Lover

        for sock in ready_read:
            #Lover is came
            #print("Lover came... can you tell me I Lub You.....")
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print("Client {} : {} connected...".format(addr[0],addr[1]))
                broadcast(server_socket, client_socket, f"{addr} entered our chatting room...\n")
                # Print the actual port number
                # print(f"Server socket port: {server_socket.getsockname()[1]}")
            else:
                try:
                    #print("Waiting for msg.....")
                    data = sock.recv(RECEIVE_BUFF)
                    data = data.decode()
                    #print("Msg: " + data)
                    #data = data.decode()
                    if data:
                        broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(), data))
                    else:
                        # The Socket must have been broken, remove it from the list, and broadband a message
                        broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(),"Client is Offline...\n")) 
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                except (s.error, ConnectionResetError) as e:
                    #print(f"Error reading data from {sock.getpeername()}: {e}")
                    #broadcast(server_socket, sock, f"[{sock.getpeername()}] Client is offline, exception \n")
                    print(f"Error reading data from {sock.getpeername()}: {e}")
                    broadcast(server_socket, sock, f"[{sock.getpeername()}] Client is offline, exception: {e}\n")
                    continue
    #TODO: Plan exit strategy
    #server_socket.close()

def broadcast(server_socket, client_socket, message):
    print("Brodcast: " + message)
    for socket in SOCKET_LIST:
        #print(SOCKET_LIST)
        if socket != server_socket and socket != client_socket:
            try:
                socket.send(message.encode())
                #socket.flush()
            except:
                #It Should be broken Connection
                socket.close()
                if socket in SOCKET_LIST:
                        SOCKET_LIST.remove(socket)

if __name__ == "__main__":
    sys.exit(chat_server())
