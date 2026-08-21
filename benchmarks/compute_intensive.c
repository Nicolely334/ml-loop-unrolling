#include <stdio.h>
#include <math.h>

// Compute-intensive loop - likely benefits from unrolling
int main() {
    double sum = 0.0;
    
    for (int i = 0; i < 100000; i++) {
        double x = (double)i / 1000.0;
        sum += x * x * x - 2 * x * x + x - 5;
    }
    
    printf("%f\n", sum);
    return 0;
}
