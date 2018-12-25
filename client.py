import socket
from pickle import dumps, loads
from ui import window
import signal

def s2b(s):
	s = s + (' '*(1024-len(s)))
	return bytes(s, 'utf-8')

def b2s(s):
	return s.decode("utf-8").strip()

def handler(sig, frame):
	print('you exited')
	sys.exit(0)


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = '127.0.0.1'
port  = 8000

clientsocket.connect((hostname, port))        # Bind to the port

msg = b2s(clientsocket.recv(1024)).strip()
print('SERVER >> ', msg)
signal.signal(signal.SIGINT, handler)

while True:
		print('\n')
		msg = b2s(clientsocket.recv(1024)).strip()
		print('SERVER >> ', msg)
		msg = loads(clientsocket.recv(1024))
		print(msg)
		
		window(msg)
		print('startig to read')
		with open('qt') as f:
			msg = s2b(str(f.read()))

		#msg = s2b(input('CLIENT >> '))
		clientsocket.send(msg)
		
		msg = b2s(clientsocket.recv(1024))
		print('SERVER >>', msg)
		if input('do you want to continue(y)') != 'y':
			break
		
clientsocket.close()