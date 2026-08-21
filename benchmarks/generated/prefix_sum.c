#include <stdio.h>
#include <stdlib.h>

#define N 50000

int main() {
    int *arr = malloc(N * sizeof(int));
    int *prefix = malloc(N * sizeof(int));
    
    for (int i = 0; i < N; i++)
        arr[i] = i + 1;
    
    prefix[0] = arr[0];
    for (int i = 1; i < N; i++) {
        prefix[i] = prefix[i-1] + arr[i];  // dependency chain
    }
    
    printf("%d\n", prefix[N-1]);
    free(arr); free(prefix);
    return 0;
}
