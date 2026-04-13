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

int main(int argc, char **argv)
{
    int rank, size;
    int num_arg;
    int *my_vector = NULL;
    int chunk_size;
    int start_index, end_index;
    int local_sum = 0;
    int global_sum = 0;
    double start, end;

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
    start_index = rank * chunk_size;
    end_index = start_index + chunk_size;

    my_vector = malloc(num_arg * sizeof(int));
    if (my_vector == NULL)
    {
        fprintf(stderr, "Memory allocation failed on rank %d.\n", rank);
        MPI_Finalize();
        exit(-1);
    }

    if (rank == 0)
    {
        for (int i = 0; i < num_arg; i++)
        {
            my_vector[i] = i + 1;
        }
    }

    start = MPI_Wtime();

    MPI_Bcast(my_vector, num_arg, MPI_INT, 0, MPI_COMM_WORLD);

    for (int i = start_index; i < end_index; i++)
    {
        local_sum += my_vector[i];
    }

    MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    end = MPI_Wtime();

    if (rank == 0)
    {
        printf("Sum: %d\n", global_sum);
        printf("Internal runtime: %f\n", end - start);
    }

    free(my_vector);

    MPI_Finalize();
    return 0;
}
