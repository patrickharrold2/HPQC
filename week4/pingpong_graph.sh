#!/bin/bash

OUTFILE="bandwidth_results.csv"

echo "bytes,elapsed_time,average_time" > "$OUTFILE"

for size in 8 64 512 4096 32768 262144 1048576
do
    output=$(mpirun -np 2 ~/bin/pingpong_bandwidth 10000 $size)

    elapsed=$(echo "$output" | grep "Elapsed time" | awk '{print $4}')
    avg=$(echo "$output" | grep "Average time per ping-pong" | awk '{print $6}')

    echo "$size,$elapsed,$avg" >> "$OUTFILE"
done

echo "Done. Results saved to $OUTFILE"
