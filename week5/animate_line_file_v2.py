import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import sys

def animate(time, data, rope):
    x_positions = np.arange(len(data.columns) - 2)
    y_positions = data.iloc[time, 2:].values
    rope.set_data(x_positions, y_positions)
    return rope,

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 animate_line_file.py <input_csv> <output_gif>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        data = pd.read_csv(input_file, skipinitialspace=True)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    num_times = len(data)

    x_positions = np.arange(len(data.columns) - 2)
    y_positions = data.iloc[0, 2:].values

    fig, ax = plt.subplots()
    ax.set_ylim(-1.1, 1.1)

    rope, = ax.plot(x_positions, y_positions, "o", markersize=5)

    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=num_times,
        interval=40,
        blit=True,
        fargs=(data, rope)
    )

    ani.save(output_file, writer="pillow", fps=25)

if __name__ == "__main__":
    main()
