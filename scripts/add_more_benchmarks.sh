#!/bin/bash
# Quickly generate more diverse benchmark programs

BENCH_DIR="$(dirname "$0")/../benchmarks/generated"
mkdir -p "$BENCH_DIR"

echo "Generating additional benchmarks..."

# 1. String operations
cat > "$BENCH_DIR/string_copy.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 50000

int main() {
    char *src = malloc(SIZE);
    char *dst = malloc(SIZE);
    
    for (int i = 0; i < SIZE; i++) src[i] = 'a' + (i % 26);
    
    for (int i = 0; i < SIZE; i++) {
        dst[i] = src[i];
    }
    
    printf("%c\n", dst[SIZE-1]);
    free(src); free(dst);
    return 0;
}
EOF

# 2. Dot product
cat > "$BENCH_DIR/dot_product.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>

#define N 10000

int main() {
    double *a = malloc(N * sizeof(double));
    double *b = malloc(N * sizeof(double));
    double sum = 0;
    
    for (int i = 0; i < N; i++) {
        a[i] = i * 0.5;
        b[i] = i * 0.3;
    }
    
    for (int i = 0; i < N; i++) {
        sum += a[i] * b[i];
    }
    
    printf("%f\n", sum);
    free(a); free(b);
    return 0;
}
EOF

# 3. Polynomial evaluation
cat > "$BENCH_DIR/polynomial.c" << 'EOF'
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
EOF

# 4. Sparse array access
cat > "$BENCH_DIR/sparse_access.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>

#define N 100000

int main() {
    int *arr = calloc(N, sizeof(int));
    int sum = 0;
    
    // access every 7th element (irregular)
    for (int i = 0; i < N; i += 7) {
        arr[i] = i;
    }
    
    for (int i = 0; i < N; i += 7) {
        sum += arr[i];
    }
    
    printf("%d\n", sum);
    free(arr);
    return 0;
}
EOF

# 5. Accumulator with dependency
cat > "$BENCH_DIR/accumulator.c" << 'EOF'
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
EOF

# 6. Image blur (2D stencil)
cat > "$BENCH_DIR/blur.c" << 'EOF'
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
EOF

# 7. Histogram
cat > "$BENCH_DIR/histogram.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define BINS 256

int main() {
    int *data = malloc(N * sizeof(int));
    int hist[BINS] = {0};
    
    for (int i = 0; i < N; i++)
        data[i] = i % BINS;
    
    for (int i = 0; i < N; i++) {
        hist[data[i]]++;
    }
    
    printf("%d\n", hist[42]);
    free(data);
    return 0;
}
EOF

# 8. Prefix sum
cat > "$BENCH_DIR/prefix_sum.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>

#define N 50000

int main() {
    int *arr = malloc(N * sizeof(int));
    int *prefix = malloc(N * sizeof(int));
    
    for (int i = 0; i < N; i++)
        arr[i] = i + 1;
    
    prefix[0] = arr[0];
    for (int i = 1; i < N; i++) {
        prefix[i] = prefix[i-1] + arr[i];  // dependency chain
    }
    
    printf("%d\n", prefix[N-1]);
    free(arr); free(prefix);
    return 0;
}
EOF

# 9. Bitwise operations
cat > "$BENCH_DIR/bitcount.c" << 'EOF'
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
EOF

# 10. Conditional assignment
cat > "$BENCH_DIR/conditional.c" << 'EOF'
#include <stdio.h>
#include <stdlib.h>

#define N 30000

int main() {
    int *arr = malloc(N * sizeof(int));
    int pos = 0, neg = 0;
    
    for (int i = 0; i < N; i++)
        arr[i] = i - N/2;
    
    for (int i = 0; i < N; i++) {
        if (arr[i] > 0) pos++;
        else neg++;
    }
    
    printf("%d %d\n", pos, neg);
    free(arr);
    return 0;
}
EOF

echo "✓ Generated 10 new benchmarks in $BENCH_DIR"
ls -1 "$BENCH_DIR"
