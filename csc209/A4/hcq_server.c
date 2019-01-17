#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "hcq.h"
#include "socket.h"

#define GET_NAME 0
#define GET_TYPE 1
#define GET_COURSE 2
#define READY_T 3
#define READY_S 4



#ifndef PORT
  #define PORT 30000
#endif

struct client *users = NULL;
Ta *ta_list = NULL;
Student *stu_list = NULL;
Course *courses;  
int num_courses = 3;


int find_network_newline(const char *buf, int n);
void read_from(struct client *user);

int main(void) {
    if ((courses = malloc(sizeof(Course) * 3)) == NULL) {
        perror("malloc for course list\n");
        exit(1);
    }
    strcpy(courses[0].code, "CSC108");
    strcpy(courses[1].code, "CSC148");
    strcpy(courses[2].code, "CSC209");

    //create the client struct linked list

    struct sockaddr_in *server = init_server_addr(PORT);
    int listenfd = set_up_server_socket(server, MAX_BACKLOG);

    int max_fd = listenfd;
    fd_set all_fds;
    FD_ZERO(&all_fds);
    FD_SET(listenfd, &all_fds);

    while (1) {
        fd_set listen_fds = all_fds;
        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("server: select\n");
            exit(1);
        }

        //listen for new connections
        if (FD_ISSET(listenfd, &listen_fds)) {
            int client_fd = accept_connection(listenfd, &users);
                if(client_fd != -1){
                    if (client_fd > max_fd) {
                    max_fd = client_fd;
                }
                FD_SET(client_fd, &all_fds);
                dprintf(client_fd, "Welcome to the Help Centre, what is your name?\r\n");
            }
        }

        struct client *user = users;
        while(user != NULL) {
            if (user->sock_fd > -1 && FD_ISSET(user->sock_fd, &listen_fds)) {
                // read from client is ready, read it into the buffer
                int num_read = read(user->sock_fd, user->after, user->room);
                //if num_read == 0, the client has disconnected
                if(num_read == -1){
                    perror("read from client");
                }else if(num_read == 0){
                    if(user->state == READY_S){
                        give_up_waiting(&stu_list, user->name);
                    } else if(user->state == READY_T){
                        remove_ta(&ta_list, user->name);
                    }
                    FD_CLR(user->sock_fd, &all_fds);
                    user->sock_fd = -1;
                    disconnect_client(&users, user->name);
                }else{
                    user->inbuf += num_read;
                    int where;
                    while((where = find_network_newline(user->buf, user->inbuf)) > 0){
                        user->buf[where - 2] = '\0'; //Null terminate the buffer
                        read_from(user);
                        //update buffer info
                        user->inbuf -= where;
                        memmove(user->buf, user->buf + where, user->inbuf);
                    }
                    user->after = user->buf + user->inbuf;
                    user->room = sizeof(user->buf) - user->inbuf;

                    //if the buffer is full without a network newline, this command is defintely invalid, remove it from the buffer
                    if(user->room == 0){
                        user->inbuf = 0;
                        user->after = user->buf;
                        user->room = sizeof(user->buf);
                    }
                }
            }
            user = user->next;
        }
    }

    // Should never get here.
    return 1;
}


/*
 * Search the first n characters of buf for a network newline (\r\n).
 * Return one plus the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 */
int find_network_newline(const char *buf, int n) {
    for(int i = 0; i < n - 1; i++){
        if(buf[i] == '\r'){
            if(buf[i + 1] == '\n'){
                return i + 2;
            }
        }
    }
    return -1;
}

/* Helper Function.
 * Read a message from the client with given index and perform the required actions.
 */
void read_from(struct client *user){
    if(user->state == GET_NAME){
        strncpy(user->name, user->buf, NAME_SIZE);
        dprintf(user->sock_fd, "Welcome %s, are you a student or TA? (input 'S' or 'T')\r\n", user->name);
        user->state = GET_TYPE;
    }
    else if(user->state == GET_TYPE){
        if(strcmp(user->buf, "T") == 0){
            user->type = 'T';
            user->state = READY_T;
            add_ta(&ta_list, user->name);
            dprintf(user->sock_fd, "Valid commands for TA:\r\n\tstats\r\n\tnext\r\n\t(or use Ctrl-C to leave)\r\n");
        }else if(strcmp(user->buf, "S") == 0){
            user->type = 'S';
            user->state = GET_COURSE;
            dprintf(user->sock_fd, "Valid courses: CSC108 CSC148 CSC209\r\n");
            dprintf(user->sock_fd, "What course queue would you like to enter?\r\n");
        }else{
            dprintf(user->sock_fd, "Incorrect syntax\r\nAre you a student or TA? (input 'S' or 'T')\r\n");
        }
    }
    else if(user->state == GET_COURSE){
        if(!strcmp(user->buf, "CSC108") || !strcmp(user->buf, "CSC148") || !strcmp(user->buf, "CSC209")){
            strcpy(user->course, user->buf);
            dprintf(user->sock_fd, "You are now waiting in the queue. While you wait you can use the stats command.\r\n");
            user->state = READY_S;
            add_student(&stu_list, user->name, user->course, courses, num_courses);
        } else{
            dprintf(user->sock_fd, "Incorrect syntax\r\nWhat course queue would you like to enter?\r\n");
        }
    }else if(user->state == READY_T){
        if(strcmp(user->buf, "next") == 0){
            next_overall(user->name, &ta_list, &stu_list);
            if(find_ta(ta_list, user->name)->current_student != NULL){
                disconnect_client(&users, find_ta(ta_list, user->name)->current_student->name);
            }
        } else if(strcmp(user->buf, "stats") == 0){
            char *message = print_full_queue(stu_list);
            dprintf(user->sock_fd, "%s", message);
            free(message);
        } else{
            dprintf(user->sock_fd, "Invalid command. Valid commands for TA:\r\n\tstats\r\n\tnext\r\n\t(or use Ctrl-C to leave)\r\n"); 
        }
    }else if(user->state == READY_S){
        if(strcmp(user->buf, "stats") == 0){
            char *message = print_currently_serving(ta_list);
            dprintf(user->sock_fd, "%s", message);
            free(message);
        } else {
            dprintf(user->sock_fd, "Invalid command. Valid commands for Student:\r\n\tstats\r\n\t(or use Ctrl-C to leave)\r\n");
        }
    }
}
