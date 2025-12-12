input = """"""

banks = input.splitlines()
orderSize = 12

output = 0

for bank in banks:
  largeOrder = [(0,-1)] * orderSize
  for i,c in enumerate(bank):
    for j,l in enumerate(largeOrder):
      if i + (len(largeOrder) - (j) - 1) < len(bank) and int(c) > l[0] and (j == 0 or largeOrder[j-1][0] > 0 and largeOrder[j-1][1] != i):
        largeOrder[j] = (int(c),i)
        largeOrder = largeOrder[:j+1] + [(0,-1)]*(len(largeOrder) - (j + 1))

  lineOutput = int("".join(map(lambda x: str(x[0]),largeOrder)))
  output += lineOutput
print(output)