import pcode

#dictionaries that contain data for each problem

sum13_dict = {
    'func_name': "sum13",
    'func_call': "sum13(nums)",
    'desc': """
    Return the sum of the numbers in the array, returning 0 for an empty array. 
    Except the number 13 is very unlucky, so it does not count and numbers that come immediately after a 13 also do not count.
    """,
    'testInputs': [[1,2,2,1], [1,1], [1,2,2,1,13]],
    'tags': ["python", "arrays", "easy"],
}
sum13_dict['function'] = eval("pcode." + sum13_dict['func_name'])
sum13_dict['testInputAnswers'] = pcode.checkTestInputs(sum13_dict['function'], sum13_dict['testInputs'])

fold_dict = {
    'func_name': "fold",
    'func_call': "fold(RNA)",
    'desc': """
    fold(RNA) accepts an RNA nucleotide sequence—that is, a string made up of the letters 'A', 'U', 'G', and 'C'—as its sole argument. The function then returns a single number, which is the maximum number of matches possible in a valid folding of this RNA string.
    Notes:
    RNA folds in a way that maximizes the total number of paired bases.
    'A' on the RNA strand can pair with any 'U' on the same strand, even if adjacent. Similarly, any 'G' can pair with any 'C'. Once bases are paired, they cannot be paired again.
    When two nucleotides pair to each other, they pinch together and any bases in between them are scrunched up into a loop. Within this loop, pairing can take place. Outside of the loop on any continuous strand, pairing can also take place. Pairing cannot take place between a nucleotide inside a loop and one outside the loop!
    """,
    'testInputs': ["ACCCCCU", "AAUUGCGC", "ACUGAGCCCUGUUAGCUAA"],
    'tags': ["python", "higher-order functions", "recursion", "strings", "hard"],
}

fold_dict['function'] = eval("pcode." + fold_dict['func_name'])
fold_dict['testInputAnswers'] = pcode.checkTestInputs(fold_dict['function'], fold_dict['testInputs'])

probDict = {
    "fold": fold_dict,
    "sum13": sum13_dict
}
