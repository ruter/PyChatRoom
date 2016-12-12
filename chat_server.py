# -*- coding: utf-8 -*-

import socket, select

# Broadcast chat message to all connected clients
def broadcast_data(sock, message):
	for socket in CONNECTION_LIST:
		# Don't send message to server socket and message sender
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			# Close disconnected socket
			except:
				socket.close()
				CONNECTION_LIST.remove(socket)

if __name__ == '__main__':
	
	# List to keep track of socket descriptors
	CONNECTION_LIST = []
	RECV_BUFFER = 4096
	PORT = 10086

	# Create a TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	server_socket.bind(("0.0.0.0", PORT))
	# Listen for incoming connections
	server_socket.listen(10)

	CONNECTION_LIST.append(server_socket)

	print "Chat server started on port", PORT

	while True:
		read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

		for sock in read_sockets:
			# New connection
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr

				broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
			# New message incoming from a client
			else:
				try:
					data = sock.recv(RECV_BUFFER)
					if data:
						broadcast_data(sock, "\r<%s> %s\n" % (sock.getpeername(), data))
				except:
					broadcast_data(sock, "Client (%s, %s) is offline.\n" % addr)
					print "Client (%s, %s) is offline." % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue

	server_socket.close()