def bit_str_parser(bit_str):
    bit_str = str(bit_str)
    bit_str = bit_str[2:len(bit_str)-1]
    return bit_str

# Echo server program
import socket
from battleship import BattleShip

canDisplayColor = input("Are you using an IDE that can display color in the terminal? (y/n)") == "y"

myBattleship = BattleShip(canDisplayColor)
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

            conn.sendall(str.encode(myBattleship.send_ships_pos()))
            print("Boards have been passed, ready to play.\n")


            response = ""
            recieved = ""
            while response != "quit" or recieved != "quit":
                if can_move:
                    validPlacement = False
                    
                    # Display your board
                    if canDisplayColor:
                        myBattleship.display_board_colored()
                    else:
                        myBattleship.display_board()

                    
                    while not validPlacement:
                        try:
                            # If this is a valid placement continue, if not then have them enter again
                            response = input("\nWhere do you want to fire? (eg., a5) ")
                            myBattleship.fire_on_enemy(response)
                            validPlacement = True
                        except Exception:
                            print("\nNot a valid place, pick another spot. ")
                    
                    # Display your board
                    if canDisplayColor:
                        myBattleship.display_board_colored()
                    else:
                        myBattleship.display_board()
                    
                    can_move = False
                    
                    if len(str.encode(response)) > 1024:
                        conn.sendall(str.encode(response)[:1024])
                    else:
                        conn.sendall(str.encode(response))
                        
                    if myBattleship.has_won():
                        print("You Won!\n")
                        response = input("Would you like to play again? If not type 'quit'")
                        if response != "quit":
                            myBattleship.reset()
                        can_move = True

                        if len(str.encode(response)) > 1024:
                            conn.sendall(str.encode(response)[:1024])
                        else:
                            conn.sendall(str.encode(response))
                    
                    # s.sendto(str.encode(response), (addr[0], PORT))
                else:
                    print("Waiting for other player's response...\n")
                    recieved = conn.recv(1024).decode()

                    myBattleship.recieve_fire(recieved)

                    print("> " + recieved)
                    can_move = True
                
                    if myBattleship.has_lost():
                        print("You Lost!\n")
                        print("Waiting for players response...")
                        
                        recieved = conn.recv(1024).decode()
                        if recieved != "quit":
                            myBattleship.reset()
                        can_move = False

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
                
                validPlacement = False
                
                # Display your board
                if canDisplayColor:
                    myBattleship.display_board_colored()
                else:
                    myBattleship.display_board()

                
                while not validPlacement:
                    try:
                        # If this is a valid placement continue, if not then have them enter again
                        response = input("\nWhere do you want to fire? (eg., a5) ")
                        myBattleship.fire_on_enemy(response)
                        validPlacement = True
                    except Exception:
                        print("\nNot a valid place, pick another spot. ")
                
                # Display your board
                if canDisplayColor:
                    myBattleship.display_board_colored()
                else:
                    myBattleship.display_board()

                can_move = False

                if len(str.encode(response)) > 1024:
                    s.sendall(str.encode(response)[:1024])
                else:
                    s.sendall(str.encode(response))

                if myBattleship.has_won():
                    print("You Won!\n")
                    response = input("Would you like to play again? If not type 'quit'")
                    if response != "quit":
                        myBattleship.reset()
                    can_move = True

                    if len(str.encode(response)) > 1024:
                        s.sendall(str.encode(response)[:1024])
                    else:
                        s.sendall(str.encode(response))
                    
            else:
                print("Waiting for other player's response...\n")
                recieved = s.recv(1024).decode()
                myBattleship.recieve_fire(recieved)

                can_move = True

                if myBattleship.has_lost():
                    print("You Lost!\n")
                    print("Waiting for players response...")

                    recieved = s.recv(1024).decode()
                    if recieved != "quit":
                        myBattleship.reset()
                    can_move = False

                print("> " + recieved)
                