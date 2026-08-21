#include <stdio.h>
#include <stdlib.h>

// 2D Jacobi stencil - iterative solver
// Memory-intensive with regular access pattern

#define N 256
#define TSTEPS 40

int main() {
    double **A = malloc(N * sizeof(double*));
    double **B = malloc(N * sizeof(double*));
    
    for (int i = 0; i < N; i++) {
        A[i] = malloc(N * sizeof(double));
        B[i] = malloc(N * sizeof(double));
    }
    
    // init
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            A[i][j] = ((double) i*(j+2) + 2) / N;
    
    // iterate - stencil pattern
    for (int t = 0; t < TSTEPS; t++) {
        for (int i = 1; i < N-1; i++) {
            for (int j = 1; j < N-1; j++) {
                B[i][j] = 0.2 * (A[i][j] + A[i][j-1] + A[i][1+j] + A[1+i][j] + A[i-1][j]);
            }
        }
        for (int i = 1; i < N-1; i++) {
            for (int j = 1; j < N-1; j++) {
                A[i][j] = 0.2 * (B[i][j] + B[i][j-1] + B[i][1+j] + B[1+i][j] + B[i-1][j]);
            }
        }
    }
    
    printf("%f\n", A[N/2][N/2]);
    
    for (int i = 0; i < N; i++) {
        free(A[i]); free(B[i]);
    }
    free(A); free(B);
    
    return 0;
}
