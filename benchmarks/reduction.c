#include <stdio.h>

// Reduction pattern - classic unrolling candidate
int main() {
    long product = 1;
    
    for (int i = 1; i < 20; i++) {
        product *= i;
    }
    
    printf("%ld\n", product);
    return 0;
}
