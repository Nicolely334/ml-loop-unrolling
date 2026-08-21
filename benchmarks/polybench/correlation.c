#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Correlation coefficient computation
// Mix of reduction and nested loops

#define M 200  // samples
#define N 80   // features

int main() {
    double **data = malloc(N * sizeof(double*));
    double *mean = calloc(M, sizeof(double));
    double *stddev = calloc(M, sizeof(double));
    double **corr = malloc(M * sizeof(double*));
    
    for (int i = 0; i < N; i++)
        data[i] = malloc(M * sizeof(double));
    for (int i = 0; i < M; i++)
        corr[i] = calloc(M, sizeof(double));
    
    // init data
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            data[i][j] = (double)(i*j) / M;
    
    // compute mean
    for (int j = 0; j < M; j++) {
        for (int i = 0; i < N; i++)
            mean[j] += data[i][j];
        mean[j] /= N;
    }
    
    // compute stddev
    for (int j = 0; j < M; j++) {
        for (int i = 0; i < N; i++)
            stddev[j] += (data[i][j] - mean[j]) * (data[i][j] - mean[j]);
        stddev[j] /= N;
        stddev[j] = sqrt(stddev[j]);
        if (stddev[j] <= 0.1) stddev[j] = 1.0;
    }
    
    // normalize
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            data[i][j] -= mean[j];
    
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            data[i][j] /= sqrt(N) * stddev[j];
    
    // correlation matrix
    for (int i = 0; i < M-1; i++) {
        corr[i][i] = 1.0;
        for (int j = i+1; j < M; j++) {
            for (int k = 0; k < N; k++)
                corr[i][j] += data[k][i] * data[k][j];
            corr[j][i] = corr[i][j];
        }
    }
    corr[M-1][M-1] = 1.0;
    
    printf("%f\n", corr[M/2][M/2+1]);
    
    for (int i = 0; i < N; i++) free(data[i]);
    for (int i = 0; i < M; i++) free(corr[i]);
    free(data); free(mean); free(stddev); free(corr);
    
    return 0;
}
