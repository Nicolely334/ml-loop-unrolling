#include <stdio.h>

// Medium loop with moderate computation
int main() {
    long sum = 0;
    
    for (int i = 0; i < 10000; i++) {
        sum += i * i + i * 3 - i / 2;
    }
    
    printf("%ld\n", sum);
    return 0;
}
