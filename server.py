import socket               # Import socket module
import _thread as thread
from pickle import dumps, loads
import signal 
import sys

def s2b(s):
	s = s + (' '*(1024-len(s)))
	return bytes(s, 'utf-8')

def b2s(s):
	return s.decode("utf-8").strip()

def handler(sig, frame):
	print('\nfinal available seats :', tickets, '\n')
	print('here are your final booked seats (user : seat_no) :', booked)
	sys.exit(0)

def on_new_client(clientsocket, addr, tickets):
	global lock, booked
	clientsocket.send(s2b("WELCOME - "+str(addr)+'\n'))

	while True:

		try:
			clientsocket.send(s2b('here are our available seats, select one among them : '))
		except BrokenPipeError:
			print('client', addr, 'exited')
			clientsocket.close()
			break

		clientsocket.send(dumps(tickets))
		
		flag = 0

		try:
			msg = b2s(clientsocket.recv(1024))
		except ConnectionResetError:
			print('client', addr, 'exited')
			clientsocket.close()
			break
		
		lock.acquire()

		if msg == 'q':
			clientsocket.close()

		if msg == '':
			msg = s2b('invalid entry')
			clientsocket.send(msg)
			lock.release()
			continue

		print('CLIENT({}) >> {}'.format((addr[1]), msg))
		
		for i in msg:
			if ord(i)<48 or ord(i)>57:
				msg = s2b('invalid entry')
				clientsocket.send(msg)
				flag = 1
				break

		if flag == 0:
			if int(msg) in tickets:
				tickets.remove(int(msg))
				booked[int(msg)] = addr
				msg = s2b('your ticket successfully booked')
				clientsocket.send(msg)
			else:
				msg = s2b('seat number not available')
				clientsocket.send(msg)	
		lock.release()
		#print('CLIENT({}) >> {}'.format((addr[1]), msg))
		
	clientsocket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '127.0.0.1'
port = 8000                # Reserve a port for your service.

print('Server started on addr : !', host)
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
tickets = [i for i in range(1, 21)]
booked = dict()

signal.signal(signal.SIGINT, handler)
print('press CTRL+C to exit')

lock = thread.allocate_lock()

while True:
   c, addr = s.accept()     # Establish connection with client.
   print('\nGot connection from', addr)
   thread.start_new_thread(on_new_client, (c, addr, tickets))
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
print(booked)
s.close()
