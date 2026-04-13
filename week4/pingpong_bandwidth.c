#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int check_args(int argc, char **argv, int my_rank)
{
    if (argc != 3)
    {
        if (my_rank == 0)
            printf("Usage: mpirun -np 2 ~/bin/pingpong_bandwidth <num_pings> <num_bytes>\n");
        return 1;
    }
    return 0;
}

int check_uni_size(int uni_size, int my_rank)
{
    if (uni_size != 2)
    {
        if (my_rank == 0)
            printf("This program must be run with exactly 2 processes.\n");
        return 1;
    }
    return 0;
}

int check_num_bytes(int num_bytes, int my_rank)
{
    if (num_bytes < (int)sizeof(int))
    {
        if (my_rank == 0)
            printf("num_bytes must be at least %lu bytes.\n", sizeof(int));
        return 1;
    }
    return 0;
}

int main(int argc, char **argv)
{
    int my_rank, uni_size;
    int num_pings, num_bytes, num_elements;
    int tag = 0;
    int counter = 0;
    int *data = NULL;
    double start_time, end_time, elapsed_time, average_time;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &uni_size);

    if (check_uni_size(uni_size, my_rank))
    {
        MPI_Finalize();
        return 1;
    }

    if (check_args(argc, argv, my_rank))
    {
        MPI_Finalize();
        return 1;
    }

    num_pings = atoi(argv[1]);
    num_bytes = atoi(argv[2]);

    if (check_num_bytes(num_bytes, my_rank))
    {
        MPI_Finalize();
        return 1;
    }

    num_elements = num_bytes / sizeof(int);
    if (num_elements < 1)
        num_elements = 1;

    data = (int *)malloc(num_elements * sizeof(int));
    if (data == NULL)
    {
        if (my_rank == 0)
            printf("Memory allocation failed.\n");
        MPI_Finalize();
        return 1;
    }

    for (int i = 0; i < num_elements; i++)
        data[i] = i;

    if (my_rank == 0)
        start_time = MPI_Wtime();

    while (counter < num_pings)
    {
        if (my_rank == 0)
        {
            data[0] = counter;
            MPI_Send(data, num_elements, MPI_INT, 1, tag, MPI_COMM_WORLD);
            MPI_Recv(data, num_elements, MPI_INT, 1, tag, MPI_COMM_WORLD, &status);
            counter = data[0];
        }
        else if (my_rank == 1)
        {
            MPI_Recv(data, num_elements, MPI_INT, 0, tag, MPI_COMM_WORLD, &status);
            counter = data[0] + 1;
            data[0] = counter;
            MPI_Send(data, num_elements, MPI_INT, 0, tag, MPI_COMM_WORLD);
        }
    }

    if (my_rank == 0)
    {
        end_time = MPI_Wtime();
        elapsed_time = end_time - start_time;
        average_time = elapsed_time / num_pings;

        printf("Message size = %d bytes\n", num_elements * (int)sizeof(int));
        printf("Final counter = %d\n", counter);
        printf("Elapsed time = %lf s\n", elapsed_time);
        printf("Average time per ping-pong = %lf s\n", average_time);
    }

    free(data);
    MPI_Finalize();
    return 0;
}
