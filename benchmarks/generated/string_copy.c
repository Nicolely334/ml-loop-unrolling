#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 50000

int main() {
    char *src = malloc(SIZE);
    char *dst = malloc(SIZE);
    
    for (int i = 0; i < SIZE; i++) src[i] = 'a' + (i % 26);
    
    for (int i = 0; i < SIZE; i++) {
        dst[i] = src[i];
    }
    
    printf("%c\n", dst[SIZE-1]);
    free(src); free(dst);
    return 0;
}
