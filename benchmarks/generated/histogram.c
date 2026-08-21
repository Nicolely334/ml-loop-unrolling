#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define BINS 256

int main() {
    int *data = malloc(N * sizeof(int));
    int hist[BINS] = {0};
    
    for (int i = 0; i < N; i++)
        data[i] = i % BINS;
    
    for (int i = 0; i < N; i++) {
        hist[data[i]]++;
    }
    
    printf("%d\n", hist[42]);
    free(data);
    return 0;
}
