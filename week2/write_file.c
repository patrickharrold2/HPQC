#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    int n = atoi(argv[1]);

    FILE *f = fopen("data.txt", "w");

    clock_t start = clock();

    for (int i = 0; i < n; i++) {
        fprintf(f, "%d\n", i);
    }

    clock_t end = clock();

    fclose(f);

    double time_taken = (double)(end - start) / CLOCKS_PER_SEC;
    printf("%f\n", time_taken);

    return 0;
}
