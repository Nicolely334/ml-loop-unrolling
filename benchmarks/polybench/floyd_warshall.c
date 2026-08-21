#include <stdio.h>
#include <stdlib.h>

// Floyd-Warshall all-pairs shortest path
// Triply nested with data dependencies

#define N 180

int main() {
    int **path = malloc(N * sizeof(int*));
    
    for (int i = 0; i < N; i++) {
        path[i] = malloc(N * sizeof(int));
    }
    
    // init with distances
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            path[i][j] = (i+j) % 13 + 1;
            if (i == j) path[i][j] = 0;
        }
    }
    
    // floyd-warshall - loop-carried dependency
    for (int k = 0; k < N; k++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (path[i][j] > path[i][k] + path[k][j])
                    path[i][j] = path[i][k] + path[k][j];
            }
        }
    }
    
    printf("%d\n", path[N/2][N/3]);
    
    for (int i = 0; i < N; i++) free(path[i]);
    free(path);
    
    return 0;
}
