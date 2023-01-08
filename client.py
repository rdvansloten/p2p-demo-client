import socket
import threading
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--client-port', type=int, required=False, help='Port to run the client on.')
parser.add_argument('--server-port', type=int, required=False, help='Port to connect to the server on.')
args = parser.parse_args()

client_port = args.client_port
server_port = args.server_port

if not args.client_port:
  client_port = os.environ.get('CLIENT_PORT')

if not args.server_port:
  server_port = os.environ.get('SERVER_PORT')

server = ('0.0.0.0', server_port)

# connect to server
print('Connecting to server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.bind(('0.0.0.0', client_port))
sock.sendto(b'0', server)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('Checked in with server, waiting...')
        break

data = sock.recv(1024).decode()
print(data)
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\nGot peer')
print('  IP address:         {}'.format(ip))
print('  Source port:        {}'.format(sport))
print('  Destination port:   {}\n'.format(dport))

# punch hole
print('Punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))