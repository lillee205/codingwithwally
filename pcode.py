def correctFunc(nums):
  if len(nums) == 0:
    return 0
  newArr = [nums[0]]
  for i in range(1,len(nums)):
    if nums[i-1] != 13:
      newArr += [nums[i]]
  return sum(filter(lambda x: x != 13, newArr))

def checkAnswers(code, correctFunc, inputs):
  exec(code) #turns string that you wrote into textbook into actual function
  nameDef = code[4:code.index("(")] #grab the name of the function so you can call it, since you defined it above
  correctAns = []
  testAns = []
  for i in range(len(inputs)):
    correctAns += [correctFunc(inputs[i])]
    hella = nameDef+'({})'.format(inputs[i])
    print("hella is " + str(hella))
    testAns += [eval(hella)]
  return correctAns, testAns

