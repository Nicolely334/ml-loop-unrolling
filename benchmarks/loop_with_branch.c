#include <stdio.h>

// Loop with conditional branch - control flow affects unrolling benefit
int main() {
    long sum = 0;
    
    for (int i = 0; i < 50000; i++) {
        if (i % 2 == 0) {
            sum += i * i;
        } else {
            sum += i;
        }
    }
    
    printf("%ld\n", sum);
    return 0;
}
