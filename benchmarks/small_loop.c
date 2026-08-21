#include <stdio.h>

// Small loop - likely benefits from unrolling
int main() {
    long sum = 0;
    
    for (int i = 0; i < 100; i++) {
        sum += i * i;
    }
    
    printf("%ld\n", sum);
    return 0;
}
