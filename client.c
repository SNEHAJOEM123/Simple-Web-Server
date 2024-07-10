#include <stdio.h>
#include <stdlib.h> // Added for exit() function
#include <string.h> // Added for strlen() function
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>

#define SERVER_PORT 5432
#define MAX_LINE 256

int main(int argc, char * argv[]) {
    FILE *fp; // Unused variable, can be removed
    struct hostent *hp; // Structure to hold host information
    struct sockaddr_in sin; // Structure to hold server address information
    char *host; // Hostname of the server
    char buf[MAX_LINE]; // Buffer to hold data to send and receive
    int s; // Socket descriptor
    int len; // Length of received data

    // Check if correct number of arguments is provided
    if (argc != 2) {
        fprintf(stderr, "usage: simplex-talk host\n"); // Print usage message to stderr
        exit(1); // Exit program with error code
    }

    host = argv[1]; // Retrieve hostname from command-line arguments

    // Translate host name into peer's IP address
    hp = gethostbyname(host);
    if (!hp) { // Check if host information is retrieved successfully
        fprintf(stderr, "simplex-talk: unknown host: %s\n", host); // Print error message to stderr
        exit(1); // Exit program with error code
    }

    // Build address data structure
    bzero((char *)&sin, sizeof(sin)); // Initialize server address structure to zero
    sin.sin_family = AF_INET; // Address family (IPv4)
    bcopy(hp->h_addr, (char *)&sin.sin_addr, hp->h_length); // Copy server IP address from hostent structure
    sin.sin_port = htons(SERVER_PORT); // Convert port number to network byte order

    // Active open: Create socket and connect to server
    if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0) { // Create socket
        perror("simplex-talk: socket"); // Print error message to stderr
        exit(1); // Exit program with error code
    }
    if (connect(s, (struct sockaddr *)&sin, sizeof(sin)) < 0) { // Connect to server
        perror("simplex-talk: connect"); // Print error message to stderr
        close(s); // Close socket
        exit(1); // Exit program with error code
    }

    // Main loop: get and send lines of text
    while (fgets(buf, sizeof(buf), stdin)) { // Read input lines from stdin
        buf[MAX_LINE-1] = '\0'; // Ensure null-terminated string
        len = strlen(buf) + 1; // Calculate length of string including null character

        /* send line to server */
        send(s, buf, len, 0); // Send input line to server

        /* receive line from server */
        len = recv(s, buf, sizeof(buf), 0); // Receive response from server
        if (len > 0) {
            printf("Server sent back : %s", buf); // Print received message from server
        }
    }

    close(s); // Close socket
    return 0; // Exit program
}
