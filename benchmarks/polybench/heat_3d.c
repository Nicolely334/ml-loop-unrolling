#include <stdio.h>
#include <stdlib.h>

// 3D heat diffusion - 7-point stencil
// Triple-nested spatial loops

#define N 60
#define TSTEPS 20

int main() {
    double ***A = malloc(N * sizeof(double**));
    double ***B = malloc(N * sizeof(double**));
    
    for (int i = 0; i < N; i++) {
        A[i] = malloc(N * sizeof(double*));
        B[i] = malloc(N * sizeof(double*));
        for (int j = 0; j < N; j++) {
            A[i][j] = malloc(N * sizeof(double));
            B[i][j] = malloc(N * sizeof(double));
        }
    }
    
    // init
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                A[i][j][k] = (double)(i + j + (N-k)) * 10 / N;
    
    // time steps
    for (int t = 1; t <= TSTEPS; t++) {
        for (int i = 1; i < N-1; i++) {
            for (int j = 1; j < N-1; j++) {
                for (int k = 1; k < N-1; k++) {
                    B[i][j][k] = 0.125 * (A[i+1][j][k] - 2.0 * A[i][j][k] + A[i-1][j][k])
                               + 0.125 * (A[i][j+1][k] - 2.0 * A[i][j][k] + A[i][j-1][k])
                               + 0.125 * (A[i][j][k+1] - 2.0 * A[i][j][k] + A[i][j][k-1])
                               + A[i][j][k];
                }
            }
        }
        for (int i = 1; i < N-1; i++) {
            for (int j = 1; j < N-1; j++) {
                for (int k = 1; k < N-1; k++) {
                    A[i][j][k] = 0.125 * (B[i+1][j][k] - 2.0 * B[i][j][k] + B[i-1][j][k])
                               + 0.125 * (B[i][j+1][k] - 2.0 * B[i][j][k] + B[i][j-1][k])
                               + 0.125 * (B[i][j][k+1] - 2.0 * B[i][j][k] + B[i][j][k-1])
                               + B[i][j][k];
                }
            }
        }
    }
    
    printf("%f\n", A[N/2][N/2][N/2]);
    
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            free(A[i][j]); free(B[i][j]);
        }
        free(A[i]); free(B[i]);
    }
    free(A); free(B);
    
    return 0;
}
