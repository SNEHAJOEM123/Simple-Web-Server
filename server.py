import socket

# Define server host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

def handle_client(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(1024).decode()
    print("Received request:", request_data)

    # Check if request is a GET request
    if request_data.startswith("GET"):
        # Send HTTP response with name and roll number
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><title>Simple HTTP Server</title></head>
<body>
<h1>Hello!</h1>
<p>Name: Sneha Joe M</p>
<p>Roll Number: B210626EC</p>
</body>
</html>
"""
    elif request_data.startswith("POST"):
        # Parse POST data
        content_length_start = request_data.find('Content-Length:')
        content_length_end = request_data.find('\r\n', content_length_start)
        content_length = int(request_data[content_length_start + len('Content-Length:'):content_length_end])

        # Extract POST data from request
        body_start = request_data.find('\r\n\r\n') + 4
        post_data = request_data[body_start:body_start + content_length]

        # Send HTTP response with POST data
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><title>Simple HTTP Server</title></head>
<body>
<p>Name: Sneha Joe M</p>
<p>Roll Number: B210626EC</p>
<p>POST Data: {}</p>
</body>
</html>
""".format(post_data)
    else:
        # Send 405 Method Not Allowed response for other methods
        response = 'HTTP/1.1 405 Method Not Allowed\n\n'

    # Send response back to the client
    client_socket.sendall(response.encode())

    # Close client connection
    client_socket.close()

def run_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to host and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Start listening for incoming connections
    server_socket.listen(5)
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            # Accept incoming connection
            client_socket, _ = server_socket.accept()
            print("Accepted connection from:", client_socket.getpeername())

            # Handle the client request
            handle_client(client_socket)
    finally:
        # Close the server socket when done
        server_socket.close()

if __name__ == "__main__":
    run_server()
