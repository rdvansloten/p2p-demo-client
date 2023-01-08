import socket

known_port = 51000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.bind(('0.0.0.0', 55555))

# Set the timeout to 5 seconds
sock.settimeout(600)

# Create a list to store the connected clients
clients = []

while True:
    try:
        # Check for incoming data
        data, address = sock.recvfrom(128)

        # Check if the client is already connected
        if address in clients:
            # Client is already connected, process the data as normal

            # Check for a disconnection message
            if data == b'disconnect':
                # Remove the client from the list
                clients.remove(address)
                continue
        else:
            # Client is not already connected, add it to the list
            clients.append(address)

        sock.sendto(b'ready', address)

        # Check if we have enough clients to start the game
        if len(clients) >= 8:
            print('got {} clients, sending details to each'.format(len(clients)))
            break
        else:
          print("Not enough people")
    except socket.timeout:
        # Timeout occurred, check the status of the clients
        for client in clients:
            # Send a ping message to the client
            sock.sendto(b'ping', client)

            try:
                # Wait for a response from the client
                response, _ = sock.recvfrom(128)
            except socket.timeout:
                # No response received, assume the client has disconnected
                clients.remove(client)
                continue

            # Client is still connected, process the response as normal
            # ...

# Send the connection details to each client
for client in clients:
    client_addr, client_port = client
    sock.sendto('{} {} {}'.format(client_addr, client_port, known_port).encode(), client)
