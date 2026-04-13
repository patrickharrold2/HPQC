#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int check_args(int argc, char **argv, int my_rank)
{
    if (argc != 2)
    {
        if (my_rank == 0)
            printf("Usage: mpirun -np 2 ~/bin/pingpong <num_pings>\n");
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

int main(int argc, char **argv)
{
    int my_rank, uni_size;
    int counter = 0;
    int num_pings;
    int tag = 0;
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

    if (my_rank == 0)
        start_time = MPI_Wtime();

    while (counter < num_pings)
    {
        if (my_rank == 0)
        {
            MPI_Send(&counter, 1, MPI_INT, 1, tag, MPI_COMM_WORLD);
            MPI_Recv(&counter, 1, MPI_INT, 1, tag, MPI_COMM_WORLD, &status);
        }
        else if (my_rank == 1)
        {
            MPI_Recv(&counter, 1, MPI_INT, 0, tag, MPI_COMM_WORLD, &status);
            counter = counter + 1;
            MPI_Send(&counter, 1, MPI_INT, 0, tag, MPI_COMM_WORLD);
        }
    }

    if (my_rank == 0)
    {
        end_time = MPI_Wtime();
        elapsed_time = end_time - start_time;
        average_time = elapsed_time / num_pings;

        printf("Final counter = %d\n", counter);
        printf("Elapsed time = %lf s\n", elapsed_time);
        printf("Average time per ping-pong = %lf s\n", average_time);
    }

    MPI_Finalize();
    return 0;
}
