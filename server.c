#include <stdio.h>
#include <stdlib.h> // Added for exit() function
#include <string.h> // Added for strlen() function
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>

#define SERVER_PORT 5432
#define MAX_PENDING 5
#define MAX_LINE 256

int main() {
    struct sockaddr_in sin; // Struct to hold server address information
    char buf[MAX_LINE]; // Buffer to hold received data
    int len; // Length of received data
    int s, new_s; // Socket descriptors for server and new connections
    socklen_t size = sizeof(sin); // Added declaration of size

    /* build address data structure */
    bzero((char *)&sin, sizeof(sin)); // Initialize server address structure to zero
    sin.sin_family = AF_INET; // Address family (IPv4)
    sin.sin_addr.s_addr = INADDR_ANY; // Accept connections from any IP address
    sin.sin_port = htons(SERVER_PORT); // Convert port number to network byte order

    /* setup passive open */
    if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0) { // Create socket
        perror("simplex-talk: socket"); // Print error message if socket creation fails
        exit(1); // Exit program
    }
    if ((bind(s, (struct sockaddr *)&sin, sizeof(sin))) < 0) { // Bind socket to address
        perror("simplex-talk: bind"); // Print error message if binding fails
        exit(1); // Exit program
    }
    listen(s, MAX_PENDING); // Listen for incoming connections

    /* wait for connection, then receive and send back text */
    while(1) { // Infinite loop to continuously accept connections
        if ((new_s = accept(s, (struct sockaddr *)&sin, &size)) < 0) { // Accept new connection
            perror("simplex-talk: accept"); // Print error message if accept fails
            exit(1); // Exit program
        }

        while ((len = recv(new_s, buf, sizeof(buf), 0)) > 0) { // Receive data from client
            /* send back received line to client */
            send(new_s, buf, len, 0); // Send received data back to client
            printf("Client sent : %s", buf); // Print received message here
        }

        close(new_s); // Close connection with client
    }
}
