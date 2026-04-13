#include <stdio.h>
#include <time.h>

int main() {
    FILE *f = fopen("data.txt", "r");
    int x;

    clock_t start = clock();

    while (fscanf(f, "%d", &x) != EOF);

    clock_t end = clock();

    fclose(f);

    double time_taken = (double)(end - start) / CLOCKS_PER_SEC;
    printf("%f\n", time_taken);

    return 0;
}


