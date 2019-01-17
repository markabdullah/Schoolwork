#ifndef _SOCKET_H_
#define _SOCKET_H_

#include <netinet/in.h>    /* Internet domain header, for struct sockaddr_in */

#define MAX_BACKLOG 5
#define BUF_SIZE 128
#define MAX_CONNECTIONS 100
#define NAME_SIZE 32

struct client{
    int sock_fd;
    char name[NAME_SIZE];
    char type;
    char course[7];
    char buf[BUF_SIZE];
    char *after; 
    int inbuf;
    int room; 
    int state;
    struct client *next;
};


struct sockaddr_in *init_server_addr(int port);
int set_up_server_socket(struct sockaddr_in *self, int num_queue);
int accept_connection(int listenfd, struct client **users);
void reset_client(struct client *user);
void disconnect_client(struct client **users, char *student_name);

#endif
