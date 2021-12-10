# # Code From https://www.youtube.com/watch?v=IbzGL_tjmv4 Most is not my own code.

# import socket

# known_port = 50002

# hostname = socket.gethostname()
# local_ip = socket.gethostbyname(hostname)
# print(local_ip)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(("0.0.0.0", 55555))

# while True:
#     clients = []

#     while True:
#         data, address = sock.recvfrom(128)

#         print("Connection from: {}".format(address))
#         clients.append(address)

#         sock.sendto(b"ready", address)

#         if len(clients) == 2:
#             print("Got 2 clients, sending details to each")
#             break

#     c1 = clients.pop()
#     c1_addr, c1_port = c1
#     c2 = clients.pop()
#     c2_addr, c2_port = c2
    
#     sock.sendto("{} {} {}".format(c1_addr, c1_port, known_port).encode(), c2)
#     sock.sendto("{} {} {}".format(c2_addr, c2_port, known_port).encode(), c1)



# Echo server program
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"your ip is {local_ip}")
# friend_ip =input("What is your friend's ip?\n")

HOST = ""          # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)