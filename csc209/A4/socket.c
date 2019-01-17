#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>     /* inet_ntoa */
#include <netdb.h>         /* gethostname */
#include <sys/socket.h>

#include "socket.h"

/*
 * Initialize a server address associated with the given port.
 */
struct sockaddr_in *init_server_addr(int port) {
    struct sockaddr_in *addr = malloc(sizeof(struct sockaddr_in));
    if(addr == NULL){
        perror("malloc for sockaddr_in");
        exit(1);
    }
    addr->sin_family = AF_INET; // Allow sockets across machines.
    addr->sin_port = htons(port); // The port the process will listen on.
    addr->sin_addr.s_addr = INADDR_ANY; // Listen on all network interfaces.
    memset(&(addr->sin_zero), 0, 8); // Clear this field; sin_zero is used for padding for the struct.

    return addr;
}

/*
 * Create and set up a socket for a server to listen on.
 */
int set_up_server_socket(struct sockaddr_in *self, int num_queue) {
    int soc = socket(AF_INET, SOCK_STREAM, 0);
    if (soc < 0) {
        perror("socket");
        exit(1);
    }

    // Make sure we can reuse the port immediately after the
    // server terminates. Avoids the "address in use" error
    int on = 1;
    int status = setsockopt(soc, SOL_SOCKET, SO_REUSEADDR,
        (const char *) &on, sizeof(on));
    if (status < 0) {
        perror("setsockopt");
        exit(1);
    }

    // Associate the process with the address and a port
    if (bind(soc, (struct sockaddr *)self, sizeof(*self)) < 0) {
        // bind failed; could be because port is in use.
        perror("bind");
        exit(1);
    }

    // Set up a queue in the kernel to hold pending connections.
    if (listen(soc, num_queue) < 0) {
        // listen failed
        perror("listen");
        exit(1);
    }

    return soc;
}


/*
 * Wait for and accept a new connection.
 * return the clients file descriptor
 */
int accept_connection(int listenfd, struct client **users) {
    int client_fd = accept(listenfd, NULL, NULL);
    if (client_fd < 0) {
        perror("server: accept");
        close(listenfd);
        exit(1);
    }

    struct client *new_client = malloc(sizeof(struct client));
    if(new_client == NULL){
        perror("malloc for client");
        exit(1);
    }
    reset_client(new_client);
    new_client->sock_fd = client_fd;
    new_client->next = *users;
    *users = new_client;

    return client_fd;
}

/* Helper to reset values in a client
*/
void reset_client(struct client *user){
    user->sock_fd = -1; 
    user->name[0] = '\0';
    user->type = '\0';
    user->course[0] = '\0';
    user->buf[0] = '\0';
    user->after = user->buf; 
    user->inbuf = 0;
    user->room = sizeof(user->buf);  
    user->state = 0;
    user->next = NULL;
}

/* Helper to disconnect a client and remove them from the linked list of users
*/
void disconnect_client(struct client **users, char *student_name){
    struct client *client_to_free = NULL;
    if(strcmp((*users)->name, student_name) == 0){
        client_to_free = *users;
        *users = (*users)->next;
    } else{
        struct client *temp = *users;
        while(temp->next != NULL && strcmp(temp->next->name, student_name) != 0){
            temp = temp->next;
        }
        client_to_free = temp->next;
        if(temp->next != NULL){
            temp->next = temp->next->next;
        }
    }
    if(client_to_free->sock_fd >= 0 && client_to_free->state == 4){
        dprintf(client_to_free->sock_fd, "It's your turn to be seen now.\nYou are being disconnected, use Ctrl-C to exit nc.\n");
    }
    free(client_to_free);
}

