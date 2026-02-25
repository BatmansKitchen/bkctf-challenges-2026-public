#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>

#define MAX_MSG_LEN 48
#define MAX_USRNAME_LEN 32

#define MAX_MESSAGES 32

#define USER "BigHippo85"

struct Message {
    char sender[MAX_USRNAME_LEN];
    char reciever[MAX_USRNAME_LEN];
    time_t timeSent;
    size_t messageLen;
    char messageBody[MAX_MSG_LEN];
};

struct IPMessage {
    char resolved_ip[INET6_ADDRSTRLEN];
    struct Message msg;
};

struct Message inbox[MAX_MESSAGES];
int n_messages = 0;

int scanf_consume_newline(const char* format, void *output) {
    int result = scanf(format, output);
    getchar();
    return result;
}


void readInbox() {
    struct Message msg;
    if (n_messages == 0) {
        puts("Inbox is empty");
        return;
    }
    for (int i = 0; i < n_messages; i++) {
        msg = inbox[i];
        printf("From: %s, %s", msg.sender, ctime(&msg.timeSent));
        fwrite(msg.messageBody, 1, msg.messageLen, stdout);
        puts("---------");
    }
}


void sendMessage() {
    struct IPMessage sentMessage;
    struct Message msg;
    strcpy(&msg.sender, USER);
    msg.timeSent = time(NULL);
    puts("Type in your message");
    printf("> ");
    fgets(msg.messageBody, MAX_MSG_LEN, stdin);
    msg.messageLen = strlen(msg.messageBody);
    puts("Who do you want to send to?");
    printf("> ");
    fgets(msg.reciever, MAX_MSG_LEN, stdin);
    msg.reciever[strcspn(msg.reciever, "\n")] = '\0';
    if (strcmp(msg.reciever, USER) == 0) {
        if (n_messages >= MAX_MESSAGES) {
            puts("Inbox is full.");
            return;
        }
        memcpy(&inbox[n_messages], &msg, sizeof(struct Message));
        puts("Message sent to self");
        n_messages++;
        return;
    }
    else {
        // SENDING MESSAGES TO OTHER USERS IS TEMPORARILY DISABLED DUE TO THE DMCA BY UMG
        // resolveUserIP(msg.reciever, sentMessage.resolved_ip);
        memcpy(&sentMessage.msg.messageBody, &msg, sizeof(msg));
        // transmitMessage(&sentMessage);
        return;
    }
}

int main() {
    int option = 0;
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("Hello '%s'\n", USER);
    while (option != -1) {
        puts("1) Send message");
        puts("2) Read Inbox");
        puts("3) Quit");
        printf("> ");
        if (scanf_consume_newline("%d", &option) != 1) {
            puts("Not a number");
            continue;
        }
        switch (option) {
            case 1:
                sendMessage();
                break;
            case 2:
                readInbox();
                break;
            case 3:
                option = -1;
                break;
        }
    }


}