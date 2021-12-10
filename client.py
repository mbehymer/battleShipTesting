def bit_str_parser(bit_str):
    bit_str = str(bit_str)
    bit_str = bit_str[2:len(bit_str)-1]
    return bit_str

# Echo server program
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

can_move = False

print(f"your ip is {local_ip}")
friend_ip =input("If you are hosting press enter, otherwise enter your peer's ip address.\n")

if friend_ip == "":
    can_move = True
    HOST = friend_ip          # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            
            data = conn.recv(1024)
            print(data)

            conn.sendall(data)


            response = ""
            recieved = ""
            while response != "quit" or recieved != "quit":
                if can_move:
                    response = input("< ")
                    can_move = False
                    # print(addr)
                    s.sendall(str.encode(response))
                    # s.sendto(str.encode(response), addr)
                else:
                    # msgTuple = s.recvfrom(1024)
                    # print(msgTuple)
                    # recieved, addr = msgTuple
                    # print("Addr", addr)
                    recieved = s.recv(1024).decode()
                    print("> " + recieved)
                    can_move = True

            # response = ""
            # while response != "quit":
            #     if
                

else:
    # The peer connecting to the host peer goes first
    can_move = False
    HOST = friend_ip 
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        msg = str.encode(input("What do you want to say? "))
        s.sendall(msg)
        data, address = s.recvfrom(1024)
        print('Received', repr(data))
        
        response = ""
        recieved = ""
        while response != "quit" or recieved != "quit":
            if can_move:
                response = input("< ")
                can_move = False
                # print(address)
                s.sendall(str.encode(response))
                # s.sendto(str.encode(response), address)
            else:
                # msgTuple = s.recvfrom(1024)
                # print(msgTuple)
                # recieved, address = msgTuple
                # print("Addr", address)
                # recieved = bit_str_parser(recieved)
                recieved = s.recv(1024).decode()
                print("> " + recieved)
                can_move = True