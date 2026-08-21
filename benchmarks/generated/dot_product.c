#include <stdio.h>
#include <stdlib.h>

#define N 10000

int main() {
    double *a = malloc(N * sizeof(double));
    double *b = malloc(N * sizeof(double));
    double sum = 0;
    
    for (int i = 0; i < N; i++) {
        a[i] = i * 0.5;
        b[i] = i * 0.3;
    }
    
    for (int i = 0; i < N; i++) {
        sum += a[i] * b[i];
    }
    
    printf("%f\n", sum);
    free(a); free(b);
    return 0;
}
