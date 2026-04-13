import time

start = time.time()

with open("data.txt", "r") as f:
    data = f.readlines()

end = time.time()

print(end - start)

