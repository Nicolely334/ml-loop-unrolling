#include <stdio.h>
#include <stdlib.h>

// Memory-intensive loop - unrolling may not help due to memory bottleneck
#define SIZE 1000000

int main() {
    int *array = (int*)malloc(SIZE * sizeof(int));
    long sum = 0;
    
    // Initialize
    for (int i = 0; i < SIZE; i++) {
        array[i] = i;
    }
    
    // Sum with memory accesses
    for (int i = 0; i < SIZE; i++) {
        sum += array[i];
    }
    
    printf("%ld\n", sum);
    free(array);
    return 0;
}
