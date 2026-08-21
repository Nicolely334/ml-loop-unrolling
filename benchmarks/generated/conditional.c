#include <stdio.h>
#include <stdlib.h>

#define N 30000

int main() {
    int *arr = malloc(N * sizeof(int));
    int pos = 0, neg = 0;
    
    for (int i = 0; i < N; i++)
        arr[i] = i - N/2;
    
    for (int i = 0; i < N; i++) {
        if (arr[i] > 0) pos++;
        else neg++;
    }
    
    printf("%d %d\n", pos, neg);
    free(arr);
    return 0;
}
