import bluetooth

def receive_bluetooth_data():
    # Create a Bluetooth socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Choose a port number and start listening
    port = 0
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Waiting for Bluetooth connection on RFCOMM channel %d" % port)

    # Accept an incoming connection
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            # Receive data (assuming 1024 bytes is sufficient)
            data = client_sock.recv(1024)
            if not data:
                break

            # Decode and print the received data
            print("Received [%s]" % data.decode('utf-8'))
    except IOError:
        pass  # Handle exceptions as needed

    print("Disconnected.")

    # Close sockets
    client_sock.close()
    server_sock.close()

if __name__ == '__main__':
    receive_bluetooth_data()
