#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

int check_args(int argc, char **argv)
{
    if (argc != 3)
    {
        fprintf(stderr, "ERROR: Correct use: %s [NUMBER] [sendrecv|gather|reduce]\n", argv[0]);
        exit(-1);
    }
    return atoi(argv[1]);
}

void check_mode(char **argv, int rank)
{
    if (
        strcmp(argv[2], "sendrecv") != 0 &&
        strcmp(argv[2], "gather") != 0 &&
        strcmp(argv[2], "reduce") != 0
    )
    {
        if (rank == 0)
        {
            fprintf(stderr, "Mode must be: sendrecv, gather, or reduce\n");
        }
        MPI_Finalize();
        exit(-1);
    }
}

int main(int argc, char **argv)
{
    int rank, size;
    int num_arg;
    int *my_vector = NULL;
    int *local_vector = NULL;
    int chunk_size;
    int local_sum = 0;
    int global_sum = 0;
    double start, end;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    num_arg = check_args(argc, argv);
    check_mode(argv, rank);

    if (num_arg % size != 0)
    {
        if (rank == 0)
        {
            fprintf(stderr, "Input must be divisible by number of processes.\n");
        }
        MPI_Finalize();
        exit(-1);
    }

    chunk_size = num_arg / size;

    local_vector = malloc(chunk_size * sizeof(int));
    if (local_vector == NULL)
    {
        fprintf(stderr, "Memory allocation failed on rank %d.\n", rank);
        MPI_Finalize();
        exit(-1);
    }

    if (rank == 0)
    {
        my_vector = malloc(num_arg * sizeof(int));
        if (my_vector == NULL)
        {
            fprintf(stderr, "Memory allocation failed on rank 0.\n");
            free(local_vector);
            MPI_Finalize();
            exit(-1);
        }

        for (int i = 0; i < num_arg; i++)
        {
            my_vector[i] = i + 1;
        }
    }

    start = MPI_Wtime();

    MPI_Scatter(my_vector, chunk_size, MPI_INT,
                local_vector, chunk_size, MPI_INT,
                0, MPI_COMM_WORLD);

    for (int i = 0; i < chunk_size; i++)
    {
        local_sum += local_vector[i];
    }

    if (strcmp(argv[2], "sendrecv") == 0)
    {
        if (rank == 0)
        {
            global_sum = local_sum;
            int recv_sum = 0;

            for (int source = 1; source < size; source++)
            {
                MPI_Recv(&recv_sum, 1, MPI_INT, source, 0, MPI_COMM_WORLD, &status);
                global_sum += recv_sum;
            }
        }
        else
        {
            MPI_Send(&local_sum, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }
    else if (strcmp(argv[2], "gather") == 0)
    {
        int *gathered_sums = NULL;

        if (rank == 0)
        {
            gathered_sums = malloc(size * sizeof(int));
            if (gathered_sums == NULL)
            {
                fprintf(stderr, "Memory allocation failed on rank 0.\n");
                free(local_vector);
                free(my_vector);
                MPI_Finalize();
                exit(-1);
            }
        }

        MPI_Gather(&local_sum, 1, MPI_INT,
                   gathered_sums, 1, MPI_INT,
                   0, MPI_COMM_WORLD);

        if (rank == 0)
        {
            global_sum = 0;
            for (int i = 0; i < size; i++)
            {
                global_sum += gathered_sums[i];
            }
            free(gathered_sums);
        }
    }
    else if (strcmp(argv[2], "reduce") == 0)
    {
        MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    }

    end = MPI_Wtime();

    if (rank == 0)
    {
        printf("Mode: %s\n", argv[2]);
        printf("Sum: %d\n", global_sum);
        printf("Internal runtime: %f\n", end - start);
    }

    free(local_vector);
    if (rank == 0)
    {
        free(my_vector);
    }

    MPI_Finalize();
    return 0;
}
