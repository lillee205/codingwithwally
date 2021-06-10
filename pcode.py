def complement(base1, base2):
    """Returns boolean indicating whether two RNA bases are complementary."""
    if base1 == "A" and base2 == "U":
        return True
    elif base1 == "U" and base2 == "A":
        return True
    elif base1 == "C" and base2 == "G":
        return True
    elif base1 == "G" and base2 == "C":
        return True
    else:
        return False


def fold(RNA):
    """returns maximum number of matches possible in valid folding of this rna string"""
    possInd = list(filter(lambda x: complement(
        RNA[0], RNA[x]), range(1, len(RNA))))
    if len(RNA) <= 1:
        return 0
    elif len(possInd) > 0:
        match = list(map(
            lambda x: 1 + fold(RNA[1:possInd[x]]) + fold(RNA[possInd[x] + 1:]), range(len(possInd))))
        return max(match)
    else:
        return fold(RNA[1:])


def sum13(nums):
    if len(nums) == 0:
        return 0
    newArr = [nums[0]]
    for i in range(1, len(nums)):
        if nums[i-1] != 13:
            newArr += [nums[i]]
    return sum(filter(lambda x: x != 13, newArr))

def checkTestInputs(func, inputs):
    correctAns = []
    for input in inputs:
        correctAns += [func(input)]
    return correctAns
    
def checkAnswers(code, inputs):
    exec(code)  # turns string that you wrote into textbook into actual function
    # grab the name of the function so you can call it, since you defined it above
    nameDef = code[4:code.index("(")]
    testAns = []
    for i in range(len(inputs)):
        func = nameDef+'("{}")'.format(inputs[i])
        testAns += [eval(func)]
    return testAns
