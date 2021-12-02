# Code From https://www.youtube.com/watch?v=IbzGL_tjmv4 Most is not my own code.
import socket
import sys
import threading

rendezvous = ("10.34.19.202", 55555)

# connect to rendezvous
print("Connecting to rendezvous server")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 50001))
sock.sendto(b"0", rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == "ready":
        print("Checked in server with server, waiting")
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(" ")
sport = int(sport)
dport = int(dport)

print("\ngot peer")
print(" ip:            {}".format(ip))
print(" source port:   {}".format(sport))
print(" dest port:     {}\n".format(dport))

# punch hole
print("punching hole")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", sport))
sock.sendto(b"0", (ip, dport))

print("ready to exchange messages\n")

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", sport))

    while True:
        data = sock.recv(1024)
        print("\rpeer: {}\n> ".format(data.decode()), end="")

listener = threading.Thread(target=listen, daemon=True)
listener.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", dport))

while True:
    msg = input("> ")
    sock.sendto(msg.encode(), (ip, sport))