
with open('input2.txt') as fd:
    lines = fd.readlines()

times = list(map(int, filter(lambda x : x.strip(' \n'), lines[0].split(":")[1].split(" "))))
distances = list(map(int, filter(lambda x : x.strip(' \n'), lines[1].split(":")[1].split(" "))))

def numberOfMilisecondsHoldingToDistanceTraveled(msHolding, totalTime):
    return (totalTime - msHolding) * (msHolding)

totalNumberOfWays = 1
for (time, distance) in zip(times, distances):
    print(f'{time}, {distance}: ')
    solutions = []
    for i in range(time + 1):
        result = numberOfMilisecondsHoldingToDistanceTraveled(i, time)
        if result > distance:
            solutions.append(result)
        print(f'{result}: {"Yes" if result > distance else "No"}')
    
    totalNumberOfWays *= len(solutions)

print(totalNumberOfWays)