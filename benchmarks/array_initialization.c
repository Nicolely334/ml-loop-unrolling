#include <stdio.h>
#include <stdlib.h>

// Array initialization - benefits from unrolling
#define SIZE 100000

int main() {
    int *array = (int*)malloc(SIZE * sizeof(int));
    
    for (int i = 0; i < SIZE; i++) {
        array[i] = i * 2;
    }
    
    printf("%d\n", array[SIZE - 1]);
    free(array);
    return 0;
}
