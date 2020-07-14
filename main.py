import pickle
import string
import time
import random

try:
    chars = pickle.load(open("charWeights.hang","rb"))
except:
    chars = {}
    for char in string.ascii_lowercase:
        chars[char] = 0

try:
    dictionary = pickle.load(open("dictionary.hang","rb"))
except:
    dictionary = []

guessedChars = []

def Sort(unsorted_):
    unsorted = {}
    for key in unsorted_:
        unsorted[key] = unsorted_[key]
    sorted = []
    while unsorted != {}:
        best = ""
        for char in unsorted:
            if best == "" or unsorted[char] > unsorted[best]:
                best = char
        sorted.append(best)
        del unsorted[best]
    return sorted

def ClosestMatch(known,p):
    closest = None
    bestMatchCount = 0
    for word in dictionary:
        if len(word) != len(known):
            continue
        match = True
        matches = 0
        for i in range(len(known)):
            if (known[i] != word[i] and known[i] != "*") or (word[i] in guessedChars and not word[i] in known[i]):
                match = False
            else:
                matches += 1
        if match and bestMatchCount < matches:
            bestMatchCount = matches
            closest = word
    if p:
        print(closest)
    if closest == None:
        consonents = {}
        vowels = {}
        for char in chars:
            if char in ["a","e","i","o","u"]:
                vowels[char] = chars[char]
            else:
                consonents[char] = chars[char]
        return Sort(vowels)+Sort(consonents),False
    else:
        consonents = {}
        vowels = {}
        for i in range(len(known)):
            if known[i] == "*" and closest[i] in ["a","e","i","o","u"]:
                vowels[closest[i]] = chars[closest[i]]
            elif known[i] == "*":
                consonents[closest[i]] = chars[closest[i]]
        remainingChars = Sort(vowels)+Sort(consonents)
        return remainingChars,True

def importWords():
    filename = input("Enter the path to the text file: ")
    with open(filename,"r") as f:
        text = f.read().lower()
        word = ""
        print("Generating dictionary...")
        print("Adjusting character weights...")
        i = 0
        p = 0.01
        st = time.time()
        for char in text:
            i += 1
            if char in string.ascii_lowercase:
                word += char
                chars[char] += 1
            elif not char in string.punctuation:
                if not word in dictionary and word != "":
                    dictionary.append(word)
                word = ""
            if i / len(text) >= p:
                print(f"{int(p*100)}% complete ETR: {(time.time()-st)*(1/p)*(1-p)} seconds")
                p += 0.01
    pickle.dump(dictionary,open("dictionary.hang","wb"))
    pickle.dump(chars,open("charWeights.hang","wb"))
    print("Import complete")


def hangman(wordToGuess,p = True):
    global guessedChars
    guessedChars = []
    wordToGuess = wordToGuess.lower()
    guessed = ["*"] * len(wordToGuess)
    consonents = {}
    vowels = {}
    for char in chars:
        if char in ["a","e","i","o","u"]:
            vowels[char] = chars[char]
        else:
            consonents[char] = chars[char]
    guessOrder = Sort(vowels)+Sort(consonents)
    nextGuess = 0
    lives = 10
    while "".join(guessed) != wordToGuess and lives > 0:
        guess = guessOrder[nextGuess]
        nextGuess += 1
        guessedChars.append(guess)
        correct = False
        for i in range(len(wordToGuess)):
            if wordToGuess[i] == guess:
                correct = True
                guessed[i] = guess
        if not correct:
            lives -= 1
        if p:
            print("".join(guessed))
        guessOrder,match = ClosestMatch(guessed,p)
        if match:
            nextGuess = 0
    if not wordToGuess in dictionary:
        dictionary.append(wordToGuess)
        pickle.dump(dictionary,open("dictionary.hang","wb"))
        for char in wordToGuess:
            chars[char] += 1
        pickle.dump(chars,open("charWeights.hang","wb"))

    return (lives > 0, lives)

if "y" in input("Import words?\n"):
    importWords()

testSetLength = 1000
if "y" in input("Test success rate?\n"):
    testSet = []
    while len(testSet) < testSetLength:
        word = random.choice(dictionary)
        if not word in testSet:
            testSet.append(word)
    wins = 0
    wrongWords = {}
    for i in range(testSetLength):
        result = hangman(testSet[i],False)
        if result[0]:
            wins += 1
        else:
            wrongWords[testSet[i]] = result[1]

        print(f"{wins/(i+1)*100}% {wins}/{i+1}/{testSetLength} -- {testSet[i]}")

    #print(wrongWords)

while True:
    print(hangman(input("Enter a word: ").lower()))
