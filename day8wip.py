import numpy as np

input = """"""

vectors = [np.fromstring(x,dtype=int, sep=',') for x in input.splitlines()]

vectorsSquaredR1 = [sum(vector ** 2) for vector in vectors] 

circuits = [np.array([x,x,1,0]) for x in np.sort(vectorsSquaredR1)]

connections = 0
targetConnections = len(circuits)/2
while connections < targetConnections:
  print("TEST")
  updatePos = -1
  popPos = -1
  updateVal = None
  updateDist = -1
  updateType = "D"
  for i in range(len(circuits)-2,0,-2):
    leftDist = circuits[i][0] - circuits[i-1][1]
    rightDist = circuits[i+1][0] - circuits[i][1]
    internalDist = circuits[i][1] - circuits[i][0]
    maxInternalConnections = 0
    if updateDist < 0:
      updateDist = leftDist
    if circuits[i][2] == 2:
      maxInternalConnections = 1
    elif circuits[i][2] > 2:
      maxInternalConnections = circuits[i][2] + max(0,(circuits[i][2]*(circuits[i][2] - 3))/2)
    isAlreadyInternal = circuits[i][3] == maxInternalConnections
    print(str(circuits[i][2]) + " " + str(circuits[i][3]) + " " + str(maxInternalConnections))
    if leftDist < rightDist and (leftDist < internalDist or isAlreadyInternal) and leftDist < updateDist:
      updateType = "A"
      updateDist = leftDist
      updatePos = i-1
      popPos = i
      updateVal = np.array([circuits[i-1][0],circuits[i][1],circuits[i-1][2] + circuits[i][2],max(circuits[i-1][3] + circuits[i][3],circuits[i-1][2] + circuits[i][2]-1)])
    elif rightDist < leftDist and (rightDist < internalDist or isAlreadyInternal) and rightDist < updateDist:
      updateType = "B"
      updateDist = rightDist
      updatePos = i
      popPos = i + 1
      updateVal = np.array([circuits[i][0],circuits[i+1][1],circuits[i][2] + circuits[i+1][2], max(circuits[i][3] + circuits[i+1][3],circuits[i][2] + circuits[i+1][2]-1)])
    elif not isAlreadyInternal and internalDist <= updateDist:
      updateType = "C"
      updateDist = internalDist
      updatePos = i
      updateVal = np.array([circuits[i][0],circuits[i][1],circuits[i][2], circuits[i][3]+1])
  connections += 1
  circuits[updatePos] = updateVal
  print(updateType)
  print(updateVal)
  if popPos >= 0:
    circuits.pop(popPos)

circuitLengths = np.sort([circuit[2] for circuit in circuits])
print(circuitLengths)
