#include <stdio.h>

// Nested loops - inner loop may benefit from unrolling
int main() {
    long sum = 0;
    
    for (int i = 0; i < 1000; i++) {
        for (int j = 0; j < 100; j++) {
            sum += i * j;
        }
    }
    
    printf("%ld\n", sum);
    return 0;
}
