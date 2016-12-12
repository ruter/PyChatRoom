# -*- coding: utf-8 -*-

import socket, select, string, sys

def prompt():
	sys.stdout.write('<You> ')
	sys.stdout.flush()

if __name__ == '__main__':

	RECV_BUFFER = 4096
	
	if len(sys.argv) < 3:
		print "Usage: python chat_client.py hostname port"
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	# Connect to remote host
	try:
		s.connect((host, port))
	except:
		print "Unable to connect."
		sys.exit()

	print "Connected to remote host. Start sending messages."
	prompt()

	while True:
		socket_list = [sys.stdin, s]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

		for sock in read_sockets:
			# Incoming message from remote server
			if sock == s:
				data = sock.recv(RECV_BUFFER)
				if not data:
					print "\nDisconnected from chat server."
					sys.exit()
				else:
					sys.stdout.write(data)
					prompt()
			else:
				msg = sys.stdin.readline()
				s.send(msg)
				prompt()
         