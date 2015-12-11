sentence = 'It is raining cats and dogs'
print("Original sentence is \"" + sentence + "\"")
words = sentence.split()
print("After applying split() to sentence becomes :", words)
#print(words)

lengths = map(lambda word: len(word), words)
lengths = list(lengths)
print("Then after mapped's applying len() to workds becomes :", lengths)