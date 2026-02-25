#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define MAX_ANSWER_LEN 64

void win() {
    puts("getittwisted:");
    FILE *f = fopen("flag", "r");
    int c;
    while ((c = fgetc(f)) != EOF) putchar(c);
    putchar('\n');
}

void name() {
    char answer[32];
    while (1) {
        puts("Name a movie.");
        printf("> ");
        fgets(answer, MAX_ANSWER_LEN, stdin);
        answer[strcspn(answer, "\n")] = '\0';
        if (strcmp(answer, "Happy Gilmore") == 0) {
            puts("Now that's cinema.");
            return; 
        }
        puts("Not cinema.");
    }
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    name();
}