#include <stdio.h>
#include <stdlib.h>

#define N 100000

int main() {
    int *arr = calloc(N, sizeof(int));
    int sum = 0;
    
    // access every 7th element (irregular)
    for (int i = 0; i < N; i += 7) {
        arr[i] = i;
    }
    
    for (int i = 0; i < N; i += 7) {
        sum += arr[i];
    }
    
    printf("%d\n", sum);
    free(arr);
    return 0;
}
