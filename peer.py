def bit_str_parser(bit_str):
    bit_str = str(bit_str)
    bit_str = bit_str[2:len(bit_str)-1]
    return bit_str

# Echo server program
import socket
from battleship import BattleShip


myBattleship = BattleShip()
colors = myBattleship.Colors()

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

can_move = False

print(f"your ip is {local_ip}")
friend_ip = input("If you are hosting press enter, otherwise enter your peer's ip address.\n")

if friend_ip == "":
    print("Host is ready... \n")
    can_move = True
    HOST = friend_ip          # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            print("LET's PLAY BATTLESHIP\n")
            
            data = conn.recv(1024)
            myBattleship.load_enemy_pos(data.decode())
            # print(data)

            conn.sendall(str.encode(myBattleship.send_ships_pos()))
            print("Boards have been passed, ready to play.\n")


            response = ""
            recieved = ""
            while response != "quit" or recieved != "quit":
                if can_move:
                    
                    # Display your board
                    print(f"{colors.OKBLUE}YOUR BOARD:{colors.ENDC}\n")
                    myBattleship.show_your_colored_board()

                    # Display your view of enemies board
                    print(f"\n{colors.FAIL}ENEMY BOARD:{colors.ENDC}\n")
                    myBattleship.show_enemy_colored_board()
                    response = input("\nWhere do you want to fire? (eg., a5) ")


                    myBattleship.fire_on_enemy(response)

                    
                    # Display your board
                    print(f"{colors.OKBLUE}YOUR BOARD:{colors.ENDC}\n")
                    myBattleship.show_your_colored_board()

                    # Display your view of enemies board
                    print(f"\n{colors.FAIL}ENEMY BOARD:{colors.ENDC}\n")
                    myBattleship.show_enemy_colored_board()

                    if myBattleship.has_won():
                        print("You Won!\n")
                        response = "quit"
                    
                    can_move = False
                    # print(addr)
                    if len(str.encode(response)) > 1024:
                        conn.sendall(str.encode(response)[:1024])
                    else:
                        conn.sendall(str.encode(response))
                    
                    # s.sendto(str.encode(response), (addr[0], PORT))
                else:
                    # msgTuple = s.recvfrom(1024)
                    # print(msgTuple)
                    # recieved, addr = msgTuple
                    # print("Addr", addr)
                    print("Waiting for other player's response...\n")
                    recieved = conn.recv(1024).decode()

                    myBattleship.recieve_fire(recieved)

                    print("> " + recieved)
                    can_move = True
                

else:
    # The peer connecting to the host peer goes first
    can_move = False
    HOST = friend_ip 
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("LET's PLAY BATTLESHIP\n")

        msg = str.encode(myBattleship.send_ships_pos())
        s.sendall(msg)
        # data, address = s.recvfrom(1024)
        data = s.recv(1024).decode()
        myBattleship.load_enemy_pos(data)
        print("Boards have been passed, ready to play.\n")
        # print('Received', repr(data))
        
        response = ""
        recieved = ""
        while response != "quit" or recieved != "quit":
            if can_move:
                
                # Display your board
                print(f"{colors.OKBLUE}YOUR BOARD:{colors.ENDC}\n")
                myBattleship.show_your_colored_board()

                # Display your view of enemies board
                print(f"\n{colors.FAIL}ENEMY BOARD:{colors.ENDC}\n")
                myBattleship.show_enemy_colored_board()
                response = input("\nWhere do you want to fire? (eg., a5) ")


                myBattleship.fire_on_enemy(response)

                
                # Display your board
                print(f"{colors.OKBLUE}YOUR BOARD:{colors.ENDC}\n")
                myBattleship.show_your_colored_board()

                # Display your view of enemies board
                print(f"\n{colors.FAIL}ENEMY BOARD:{colors.ENDC}\n")
                myBattleship.show_enemy_colored_board()

                if myBattleship.has_won():
                    print("You Won!\n")
                    response = "quit"

                # response = input("< ")
                can_move = False
                # print(address)
                if len(str.encode(response)) > 1024:
                    s.sendall(str.encode(response)[:1024])
                else:
                    s.sendall(str.encode(response))
                # s.sendto(str.encode(response), address)
            else:
                # msgTuple = s.recvfrom(1024)
                # print(msgTuple)
                # recieved, address = msgTuple
                # print("Addr", address)
                # recieved = bit_str_parser(recieved)
                print("Waiting for other player's response...\n")
                recieved = s.recv(1024).decode()
                myBattleship.recieve_fire(recieved)

                print("> " + recieved)
                
                can_move = True