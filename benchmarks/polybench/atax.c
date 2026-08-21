#include <stdio.h>
#include <stdlib.h>

// Matrix transpose and vector multiply
// Classic BLAS-style operation

#define M 190
#define N 210

int main() {
    double **A = malloc(M * sizeof(double*));
    double *x = malloc(N * sizeof(double));
    double *y = calloc(N, sizeof(double));
    double *tmp = calloc(M, sizeof(double));
    
    for (int i = 0; i < M; i++)
        A[i] = malloc(N * sizeof(double));
    
    // init
    for (int i = 0; i < N; i++)
        x[i] = 1 + (i / (double)N);
    
    for (int i = 0; i < M; i++)
        for (int j = 0; j < N; j++)
            A[i][j] = (double)((i+j) % N) / (5*M);
    
    // tmp := A*x
    for (int i = 0; i < M; i++)
        for (int j = 0; j < N; j++)
            tmp[i] += A[i][j] * x[j];
    
    // y := A^T * tmp
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            y[i] += A[j][i] * tmp[j];
    
    printf("%f\n", y[N/2]);
    
    for (int i = 0; i < M; i++) free(A[i]);
    free(A); free(x); free(y); free(tmp);
    
    return 0;
}
