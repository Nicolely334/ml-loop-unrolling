#include <stdio.h>

#define N 50000

int main() {
    int acc = 1;
    
    // loop-carried dependency (limits unrolling benefit)
    for (int i = 0; i < N; i++) {
        acc = acc * 2 + i;
    }
    
    printf("%d\n", acc);
    return 0;
}
