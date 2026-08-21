#include <stdio.h>

#define N 1000000

int main() {
    double x = 1.5;
    double result = 0;
    
    // evaluate x^0 + x^1 + x^2 + ... (unrolling good for this)
    double power = 1.0;
    for (int i = 0; i < 15; i++) {
        result += power;
        power *= x;
    }
    
    printf("%f\n", result);
    return 0;
}
