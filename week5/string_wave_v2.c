#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// function declarations
int check_args(int argc, char **argv, int *cycles, int *samples, char **outfile);
void initialise_vector(double vector[], int size, double initial);
void update_positions(double* positions, int points, double time);
int generate_timestamps(double* time_stamps, int time_steps, double step_size);
double driver(double time);
void print_header(FILE** p_out_file, int points);

int main(int argc, char **argv)
{
    int cycles, samples;
    char *filename;

    int points = check_args(argc, argv, &cycles, &samples, &filename);

    int time_steps = cycles * samples + 1;
    double step_size = 1.0 / samples;

    double* time_stamps = malloc(time_steps * sizeof(double));
    initialise_vector(time_stamps, time_steps, 0.0);
    generate_timestamps(time_stamps, time_steps, step_size);

    double* positions = malloc(points * sizeof(double));
    initialise_vector(positions, points, 0.0);

    FILE* out_file = fopen(filename, "w");
    if (out_file == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    print_header(&out_file, points);

    for (int i = 0; i < time_steps; i++)
    {
        update_positions(positions, points, time_stamps[i]);

        fprintf(out_file, "%d, %lf", i, time_stamps[i]);

        for (int j = 0; j < points; j++)
        {
            fprintf(out_file, ", %lf", positions[j]);
        }
        fprintf(out_file, "\n");
    }

    free(time_stamps);
    free(positions);
    fclose(out_file);

    return 0;
}

int check_args(int argc, char **argv, int *cycles, int *samples, char **outfile)
{
    if (argc != 5)
    {
        fprintf(stderr, "Usage: %s <points> <cycles> <samples> <output_file>\n", argv[0]);
        exit(-1);
    }

    int points = atoi(argv[1]);
    *cycles = atoi(argv[2]);
    *samples = atoi(argv[3]);
    *outfile = argv[4];

    return points;
}

void print_header(FILE** p_out_file, int points)
{
    fprintf(*p_out_file, "#, time");
    for (int j = 0; j < points; j++)
    {
        fprintf(*p_out_file, ", y[%d]", j);
    }
    fprintf(*p_out_file, "\n");
}

double driver(double time)
{
    return sin(time * 2.0 * M_PI);
}

void update_positions(double* positions, int points, double time)
{
    double* new_positions = malloc(points * sizeof(double));

    new_positions[0] = driver(time);

    for (int i = 1; i < points; i++)
    {
        new_positions[i] = positions[i - 1];
    }

    for (int i = 0; i < points; i++)
    {
        positions[i] = new_positions[i];
    }

    free(new_positions);
}

int generate_timestamps(double* timestamps, int time_steps, double step_size)
{
    for (int i = 0; i < time_steps; i++)
    {
        timestamps[i] = i * step_size;
    }
    return time_steps;
}

void initialise_vector(double vector[], int size, double initial)
{
    for (int i = 0; i < size; i++)
    {
        vector[i] = initial;
    }
}
