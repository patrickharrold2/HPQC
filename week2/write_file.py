import time
import sys

n = int(sys.argv[1])

start = time.time()

with open("data.txt", "w") as f:
    for i in range(n):
        f.write(str(i) + "\n")

end = time.time()

print(end - start)
