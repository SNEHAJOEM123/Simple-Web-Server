import socket

# Define server host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

def send_request(request):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send request to the server
    client_socket.sendall(request.encode())

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print("Response from server:", response)

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    # Send GET request
    get_request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    send_request(get_request)

    # Send POST request (you can modify this with actual POST data)
    post_request = "POST /submit HTTP/1.1\r\nHost: localhost\r\nContent-Length: {}\r\n\r\n{}".format(len("Hello World"), "Hello World")
    send_request(post_request)
