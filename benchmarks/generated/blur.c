#include <stdio.h>
#include <stdlib.h>

#define W 512
#define H 512

int main() {
    int **img = malloc(H * sizeof(int*));
    int **out = malloc(H * sizeof(int*));
    
    for (int i = 0; i < H; i++) {
        img[i] = malloc(W * sizeof(int));
        out[i] = malloc(W * sizeof(int));
    }
    
    // init
    for (int y = 0; y < H; y++)
        for (int x = 0; x < W; x++)
            img[y][x] = (x + y) % 256;
    
    // 3x3 box blur
    for (int y = 1; y < H-1; y++) {
        for (int x = 1; x < W-1; x++) {
            out[y][x] = (img[y-1][x-1] + img[y-1][x] + img[y-1][x+1] +
                         img[y][x-1]   + img[y][x]   + img[y][x+1] +
                         img[y+1][x-1] + img[y+1][x] + img[y+1][x+1]) / 9;
        }
    }
    
    printf("%d\n", out[H/2][W/2]);
    
    for (int i = 0; i < H; i++) {
        free(img[i]); free(out[i]);
    }
    free(img); free(out);
    return 0;
}
