
with open('input4.txt') as fd:
    lines = fd.readlines()

time = int(''.join(list(filter(lambda x : x.strip(' \n'), lines[0].split(":")[1].split(" ")))))
distance = int(''.join(list(filter(lambda x : x.strip(' \n'), lines[1].split(":")[1].split(" ")))))

def numberOfMilisecondsHoldingToDistanceTraveled(msHolding, totalTime):
    return (totalTime - msHolding) * (msHolding)

upperBound = time
lowerBound = 0

while lowerBound < distance:
    result = numberOfMilisecondsHoldingToDistanceTraveled(lowerBound, time)
    if result > distance:
        break
    else:
        lowerBound = (upperBound - lowerBound) // 2

print("After binary search:", lowerBound)

for i in range(lowerBound, -1, -1):
    result = numberOfMilisecondsHoldingToDistanceTraveled(i, time)
    if result < distance:
        lowerBound = i
        break

assert numberOfMilisecondsHoldingToDistanceTraveled(lowerBound, time) < distance

print("After linear search:", lowerBound)

while upperBound < distance:
    result = numberOfMilisecondsHoldingToDistanceTraveled(upperBound, time)
    if result > distance:
        break
    else:
        upperBound = (upperBound - lowerBound) // 2

print("After bainry search:", upperBound)

for i in range(upperBound, time + 1):
    result = numberOfMilisecondsHoldingToDistanceTraveled(i, time)
    if result < distance:
        upperBound = i
        break

assert numberOfMilisecondsHoldingToDistanceTraveled(upperBound, time) < distance

print("After linear search:", upperBound)


print(abs(upperBound - lowerBound) - 1)