# Overview

This is a battleship game that is playable over a LAN address using each others IP. The host will not have to type in an IP address but the peer that is connecting will use the host's IP addess.

This is very similar to a server to client type of deal, but in this case the host will only listen until it has made a connection with another machine. Once it has it will stop listening and just use that newly made connection or socket. 

The battleship game allows you to play and see in color, but if you can't display color you can change that.

The purpose of writing this program was to help me to learn how to get two computers to talk with each other and send and receive information and be able to use said information.

Here is my video:

[Battleship in Python Using TCP Networking](https://youtu.be/NCTPiM3ciHA)

# Network Communication

The setup I have here is for peer to peer, unless you only have one device then you would need to use a virtual machine.

I am using TCP

The messages being sent are messages or strings that have been turned into bytes. I then decode those and use the passed strings in the battleship game

# Development Environment

VS Code

Virtual Machine Ubuntu running Linux

Python - libraries include: socket

# Useful Websites

[Socket - Low Level Networking Interface](https://docs.python.org/3/library/socket.html)
[Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
[NETWORK PROGRAMMING - SERVER & CLIENT A : BASICS](https://www.bogotobogo.com/python/python_network_programming_server_client.php)
[UDP Peer-To-Peer Messaging With Python - YouTube](https://www.youtube.com/watch?v=IbzGL_tjmv4)
[P2P Programming Framework - Python](http://cs.berry.edu/~nhamid/p2p/framework-python.html)

# Future Work

* There aren't a whole lot of things that I need to improve, though I think it would be nice to add the ability to choose who goes first
* It also would be nice to make this a client to server type of deal where you can have multiple people connect to a server and then they can pair off to play a game.