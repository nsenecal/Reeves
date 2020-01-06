#current video time = total elapsed time + current time - the time the vieo was started/unpaused
result = dict()
with open("Test.txt") as file:
    for line in file:
        time, duration = line.split(",")
        result[int(time)] = int(duration.strip("\n"))
print(list(result)[2])
print(result[list(result)[2]])
