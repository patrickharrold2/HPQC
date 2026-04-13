#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

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

double driver(double time)
{
    return sin(time * 2.0 * M_PI);
}

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int cycles, samples;
    char *filename;

    int points = check_args(argc, argv, &cycles, &samples, &filename);

    int local_n = points / size;
    int remainder = points % size;

    if (rank < remainder)
        local_n++;

    double *local_positions = calloc(local_n, sizeof(double));
    double *new_positions = calloc(local_n, sizeof(double));

    int time_steps = cycles * samples + 1;
    double step_size = 1.0 / samples;

    FILE *out_file = NULL;

    if (rank == 0)
    {
        out_file = fopen(filename, "w");
        fprintf(out_file, "#, time\n");
    }

    for (int t = 0; t < time_steps; t++)
    {
        double time = t * step_size;

        double left_recv = 0.0, right_recv = 0.0;

        // exchange boundaries
        if (rank > 0)
        {
            MPI_Sendrecv(&local_positions[0], 1, MPI_DOUBLE, rank - 1, 0,
                         &left_recv, 1, MPI_DOUBLE, rank - 1, 0,
                         MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        if (rank < size - 1)
        {
            MPI_Sendrecv(&local_positions[local_n - 1], 1, MPI_DOUBLE, rank + 1, 0,
                         &right_recv, 1, MPI_DOUBLE, rank + 1, 0,
                         MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        // update positions
        for (int i = 0; i < local_n; i++)
        {
            if (rank == 0 && i == 0)
            {
                new_positions[i] = driver(time);
            }
            else if (i == 0)
            {
                new_positions[i] = left_recv;
            }
            else
            {
                new_positions[i] = local_positions[i - 1];
            }
        }

        // swap arrays
        double *temp = local_positions;
        local_positions = new_positions;
        new_positions = temp;

        // gather to root
        double *global_positions = NULL;

        if (rank == 0)
            global_positions = malloc(points * sizeof(double));

        MPI_Gather(local_positions, local_n, MPI_DOUBLE,
                   global_positions, local_n, MPI_DOUBLE,
                   0, MPI_COMM_WORLD);

        if (rank == 0)
        {
            fprintf(out_file, "%d, %lf", t, time);
            for (int i = 0; i < points; i++)
                fprintf(out_file, ", %lf", global_positions[i]);
            fprintf(out_file, "\n");

            free(global_positions);
        }
    }

    if (rank == 0)
        fclose(out_file);

    free(local_positions);
    free(new_positions);

    MPI_Finalize();
    return 0;
}

