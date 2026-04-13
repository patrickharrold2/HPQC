#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int check_args(int argc, char **argv)
{
    int num_arg = 0;
    if (argc == 2)
    {
        num_arg = atoi(argv[1]);
    }
    else
    {
        fprintf(stderr, "ERROR: Correct use: %s [NUMBER]\n", argv[0]);
        exit(-1);
    }
    return num_arg;
}

void my_sum(void *in, void *inout, int *len, MPI_Datatype *dtype)
{
    int *input = (int *)in;
    int *inout_data = (int *)inout;

    for (int i = 0; i < *len; i++)
    {
        inout_data[i] += input[i];
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
    MPI_Op my_op;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    num_arg = check_args(argc, argv);

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

    MPI_Op_create(my_sum, 1, &my_op);

    MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, my_op, 0, MPI_COMM_WORLD);

    MPI_Op_free(&my_op);

    end = MPI_Wtime();

    if (rank == 0)
    {
        printf("Mode: custom_reduce\n");
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
