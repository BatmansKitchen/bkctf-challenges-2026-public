#include <stdlib.h>
#include <stdio.h>
#include <string.h>


char bin0[8] = "bin0";
char bin1[16] = "bin1";
char bin2[32] = "bin2";
char bin3[64] = "bin3";
char bin4[128] = "bin4";
char bin5[256] = "bin5";
char bin6[512] = "bin6";
char bin7[1024] = "bin7";

char indexInput[2];

char readFormat[4] = "%lf";

char skillIssue[] = "I'm too gets for you.";

long getsIndex() {
    long index;
    int res = scanf("%ld", &index);
    getchar();
    if (res != 1)
        return -1;
    return index;
}

void readBin() {
    long binIndex;
    long formatIndex;
    void *printValue;
    char *bins[8] = {bin0, bin1, bin2, bin3, bin4, bin5, bin6, bin7};
    printf("Which bin do you want to get?\n> ");
    if ((binIndex = getsIndex()) < 0 || binIndex > 7) {
        puts("Invalid index");
        exit(1);
    }
    printf("What do you want to get the bin as ?\n1. Integer\n2. Float\n3. String\n4. Pointer\n> ");
    if ((formatIndex = getsIndex()) < 0) {
        puts("Invalid index");
        exit(1);
    }
    printValue = *(void **)(bins[binIndex]);
    switch (formatIndex) {
        case 1:
            strcpy(readFormat, "%d");
            break;
        case 2:
            strcpy(readFormat, "%lf");
            break;
        case 3:
            strcpy(readFormat, "%s");
            printValue = (void *)bins[binIndex];
            break;
        case 4:
            strcpy(readFormat, "%p");
            break;
        default:
            puts("Not an option");
            break;
    }
    printf(readFormat, printValue);
    putchar('\n');
}

void writeBin() {
    int binIndex;
    int binSize = 8;
    char *bins[8] = {bin0, bin1, bin2, bin3, bin4, bin5, bin6, bin7};
    printf("Which bin do you want to write to?\n> ");
    if ((binIndex = getsIndex()) < 0 || binIndex > 7) {
        puts("Invalid index");
        exit(1);
    }
    for (int i = 0; i < binIndex; i++) {
        binSize *= 2;
    }
    printf("Write to bin%d (Max %d bytes)\n> ", binIndex, binSize);
    gets(bins[binIndex]);
    if (strlen(bins[binIndex]) > binSize) {
        puts(skillIssue);
        exit(1);
    }
    putchar('\n');
}


int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    int option = 0;
    while (1) {
        puts("1. Get bin");
        puts("2. Write bin");
        puts("3. Exit");
        printf("> ");
        if ((option = getsIndex()) < 0) {
            puts("Invalid index");
            exit(1);
        }
        switch (option) {
            case 1:
                readBin();
                break;
            case 2:
                writeBin();
                break;
            case 3:
                exit(0);
                break;
            default:
                puts("Not an option");
                break;
        }
    }
}