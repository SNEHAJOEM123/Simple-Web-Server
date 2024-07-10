import socket

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Check if request is a GET or POST request
    if request.startswith("GET"):
        # Send HTTP response with name and roll number for GET request
        response = """\
HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head><title>Simple Web Server</title></head>
<body>
<h1>Hello! I am</h1>
<p>Name: Sneha Joe M</p>
<p>Rollno: B210626EC</p>
</body>
</html>
"""
    elif request.startswith("POST"):
        # Extract POST data from request
        body_start = request.find('\r\n\r\n') + 4
        post_data = request[body_start:]

        # Send HTTP response with name and roll number along with received POST data
        response = """\
HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head><title>Simple Web Server</title></head>
<body>
<h1>Hello! I am</h1>
<p>Name: Sneha Joe M</p>
<p>Rollno: B210626EC</p>
<p>Received POST Data: {}</p>
</body>
</html>
""".format(post_data)
    else:
        # Send 405 Method Not Allowed response for other methods
        response = 'HTTP/1.0 405 Method Not Allowed\n\n'

    # Send the HTTP response back to the client
    client_connection.sendall(response.encode())

    # Close the client connection
    client_connection.close()

# Close the server socket
server_socket.close()
