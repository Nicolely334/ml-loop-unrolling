#include <stdio.h>
#include <stdlib.h>

// Simple matrix multiply - classic triply-nested loop
// Based on PolyBench GEMM kernel

#define N 128

int main() {
    double **A = malloc(N * sizeof(double*));
    double **B = malloc(N * sizeof(double*));
    double **C = malloc(N * sizeof(double*));
    
    for (int i = 0; i < N; i++) {
        A[i] = malloc(N * sizeof(double));
        B[i] = malloc(N * sizeof(double));
        C[i] = calloc(N, sizeof(double));
    }
    
    // init
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = (double)(i * j) / N;
            B[i][j] = (double)(i + j) / N;
        }
    }
    
    // multiply - inner loop is unrolling candidate
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    // prevent optimization
    double sum = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            sum += C[i][j];
    
    printf("%f\n", sum);
    
    for (int i = 0; i < N; i++) {
        free(A[i]); free(B[i]); free(C[i]);
    }
    free(A); free(B); free(C);
    
    return 0;
}
