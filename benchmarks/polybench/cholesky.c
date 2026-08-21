#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Cholesky decomposition - triangular matrix
// Non-uniform loop bounds

#define N 200

int main() {
    double **A = malloc(N * sizeof(double*));
    
    for (int i = 0; i < N; i++) {
        A[i] = malloc(N * sizeof(double));
    }
    
    // init positive definite matrix
    for (int i = 0; i < N; i++) {
        for (int j = 0; j <= i; j++)
            A[i][j] = (double)(-j % N) / N + 1;
        for (int j = i+1; j < N; j++)
            A[i][j] = 0;
        A[i][i] = 1;
    }
    
    // make positive semi-definite
    double **B = malloc(N * sizeof(double*));
    for (int i = 0; i < N; i++)
        B[i] = calloc(N, sizeof(double));
    
    for (int r = 0; r < N; r++)
        for (int s = 0; s < N; s++)
            for (int t = 0; t < N; t++)
                B[r][s] += A[r][t] * A[s][t];
    
    // cholesky decomposition - triangular loops
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < i; j++) {
            for (int k = 0; k < j; k++)
                B[i][j] -= B[i][k] * B[j][k];
            B[i][j] /= B[j][j];
        }
        for (int k = 0; k < i; k++)
            B[i][i] -= B[i][k] * B[i][k];
        B[i][i] = sqrt(B[i][i]);
    }
    
    printf("%f\n", B[N-1][N-1]);
    
    for (int i = 0; i < N; i++) {
        free(A[i]); free(B[i]);
    }
    free(A); free(B);
    
    return 0;
}
