#include <stdio.h>

#define N 1000000

int main() {
    int total = 0;
    
    for (int i = 0; i < N; i++) {
        int x = i;
        int count = 0;
        while (x) {
            count += x & 1;
            x >>= 1;
        }
        total += count;
    }
    
    printf("%d\n", total);
    return 0;
}
