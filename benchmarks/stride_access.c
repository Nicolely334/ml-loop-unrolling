#include <stdio.h>
#include <stdlib.h>

// Strided memory access - may not benefit from unrolling
#define SIZE 100000

int main() {
    int *array = (int*)malloc(SIZE * sizeof(int));
    long sum = 0;
    
    // Initialize
    for (int i = 0; i < SIZE; i++) {
        array[i] = i;
    }
    
    // Access every 10th element
    for (int i = 0; i < SIZE; i += 10) {
        sum += array[i];
    }
    
    printf("%ld\n", sum);
    free(array);
    return 0;
}
