import numpy as np
import random 
import tkinter as tk

global length
length = 5

class Information:
    def __init__(self, wordsUsed, greens, yellows, greys):
        self.wordsUsed = wordsUsed
        self.greens = greens
        self.yellows = yellows
        self.greys = greys

class WordleSolver:
    def getSixLetterWords():
        f = open("6 Letter Words.txt")

        arr = f.read().split("\n")
        return arr
    
    def getPossibleWords():
        f = open("PossibleWords.txt", "r")

        arr = f.read().split("\n")
        return arr

    def narrowDownCrude(arr, info):
        # print(f"\t\tnewArr: {info.greys}")
        narrowedArr = arr.copy()  
        # for word in arr:
        #     for letter in word:
        #         if word.count(letter) > 1:
        #             narrowedArr.remove(word) 
        #             break
                    
        
        for word in info.wordsUsed:
            if word in narrowedArr:
                narrowedArr.remove(word)

        narrowedArr = [word for word in narrowedArr if WordleSolver.checkGreens(word, info.greens) and WordleSolver.checkYellows(word, info.yellows) and WordleSolver.checkGreys(word, info.greys)]    
        # print(narrowedArr[0:10])
        # print(f"\t{info.greys}")
        return narrowedArr

    def checkYellows(word, yellows):
        for position, letters in yellows.items():
            if not all(letter in word for letter in letters):
                return False
        for position, letters in yellows.items():
            for letter in letters:
                if word[position] == letter:
                    return False
        # print(f"{word} is good for yellows")
        return True

    def checkGreys(word, greys):
        # print(f"{word} is {all(letter not in word for letter in greys)}")
        return all(letter not in word for letter in greys)

    def checkGreens(word, required_positions):
        for position, letter in required_positions.items():
            if word[position] != letter:
                return False
        # print(f"{word} is good for greens")
        return True

    def scoreWord(word, freqDict):
        sm = 0
        for letter in word:
            if word.count(letter) > 1:
                sm -= 10000
            elif letter in freqDict:
                sm += freqDict[letter]
            
        return sm

    def infoTheory(arr):
        freqTable = [[0 for i in range(0,26)] for j in range(0,length)]
        for word in arr:
            for i in range(0, len(word)-1):
                if ord(word[i]) - 97 >= 0 and ord(word[i]) - 97 <= 26:
                    freqTable[i][ord(word[i]) - 97] += 1
        
        maxIndeces = {}
        
        for j in range(26):
            maxIndeces[chr(j + 97)] = 0
        
        for i in range(length):
            for j in range(26):
                # if maxIndeces[chr(j + 97)] < freqTable[i][j]:
                maxIndeces[chr(j + 97)] += freqTable[i][j]
        
        # print(maxIndeces)
        
        maxIndeces = dict(sorted(maxIndeces.items(), key=lambda x:x[1]))

        wordDict = {}
        for word in arr:
            wordDict[word] = WordleSolver.scoreWord(word, maxIndeces)

        wordDict = sorted(wordDict.items(), key=lambda x:x[1], reverse=True)

        wordArr = []
        for word, freq in wordDict:
            wordArr.append(word)

        return wordArr

    def newRoute(words):
        freqTable = [[0 for i in range(0,26)] for j in range(0,length)]
        for word in words:
            for i in range(0, len(word)-1):
                if ord(word[i]) - 97 >= 0 and ord(word[i]) - 97 <= 26:
                    freqTable[i][ord(word[i]) - 97] += 1
        
        maxIndeces = {}
        
        for j in range(26):
            maxIndeces[chr(j + 97)] = 0
        
        for i in range(length):
            for j in range(26):
                # if maxIndeces[chr(j + 97)] < freqTable[i][j]:
                maxIndeces[chr(j + 97)] += freqTable[i][j]
        
        # print(maxIndeces)
        
        maxIndeces = dict(sorted(maxIndeces.items(), key=lambda x:x[1]))

        wordDict = {}
        for word in words:
            wordDict[word] = WordleSolver.scoreWord(word, maxIndeces)

        wordDict = sorted(wordDict.items(), key=lambda x:x[1], reverse=True)

        wordArr = []
        for word, freq in wordDict:
            wordArr.append(word)

        return wordArr
    
    def getRandomAnswer():
        f = open("wordle-answers-alphabetical.txt", "r")

        answers = f.read().split("\n")

        return random.choice(answers)

    def checkAnswers(words):
        f = open("wordle-answers-alphabetical.txt", "r")

        answers = f.read().split("\n")
        result = []
        dbl = False
        for word in words:
            for letter in word:
                if word.count(letter) != 1:
                    dbl = True
                    break
            
            if not dbl or word in answers:
                result.append(word)
            
        return result

    def calculate_score(word, reference_letters):
        return sum(1 for char1, char2 in zip(word, reference_letters) if char1 == char2)

    def rank_words_by_score(word_list, reference_letters):
        return sorted(word_list, key=lambda word: WordleSolver.calculate_score(word, reference_letters), reverse=True)

    def getColors(word, answer):
        # print(f"{word} and {ans} in the getColors method")
        result = ""
        for i in range(len(word)):
            if word[i] == answer[i]:
                result += "2"
            elif word[i] in answer:
                result += "1"
            else:
                result += "0"
        
        return result

    def initFromAnswer(words, answer):
        # print(words)
        # numWords = ord(input("how many words?")[0]) - 48
        previousGreens = {}
        info = Information([],{},{},[])
        for i in range(len(words)):
            word = words[i]
            # word = input(f"input your #{i} word: ")
            info.wordsUsed.append(word)
            # mask = input("input the mask of the word (0 = grey, 1 = yellow, 2 = green): ")
            if i == len(words) - 2:
                previousGreens = info.greens

            for j in range(len(word)):
                letter = word[j]
                if letter == answer[j]:
                    info.greens[j] = letter
                elif letter in answer:
                    if j in info.yellows:
                        info.yellows[j].append(letter)
                    else:
                        info.yellows[j] = [letter]
                else:
                    info.greys.append(letter)
        # print(f"info.greens: {info.greens}")
        # print(info.yellows)
        if info.greens == previousGreens:
            return [info, True]

        return [info, False]
    
    def initInfo(words, masks):
        # numWords = ord(input("how many words?")[0]) - 48
        previousGreens = {}
        info = Information([],{},{},[])
        for i in range(0, len(words)):
            word = words[i]
            # word = input(f"input your #{i} word: ")
            info.wordsUsed.append(word)
            # mask = input("input the mask of the word (0 = grey, 1 = yellow, 2 = green): ")

            if i == len(words) - 2:
                previousGreens = info.greens

            for j in range(0, len(word)):
                letter = word[j]
                maskLetter = masks[i][j]
                # print(f"{letter} is {maskLetter}")
                if maskLetter == "0":
                    if word.count(letter) > 1:
                        isYellow = False
                        for k in range(0, len(word)):
                            if word[k] == letter and masks[i][k] != "0":
                                isYellow = True
                                break
                        if isYellow:
                            if j in info.yellows:
                                info.yellows[j].append(letter)
                            else:
                                info.yellows[j] = [letter]
                        elif letter not in info.greys:
                            info.greys.append(letter)
                    else:
                        info.greys.append(letter)
                elif maskLetter == "1":
                    if j in info.yellows:
                        info.yellows[j].append(letter)
                    else:
                        info.yellows[j] = [letter]
                else:
                    info.greens[j] = letter

        if previousGreens == info.greens:
            return [info, True]
        # print(info.yellows)
        return [info, False]

global ans
def createAnswer():
    global ans
    ans = WordleSolver.getRandomAnswer()
    isDouble = True
    while isDouble:
        isDouble = False
        for letter in ans:
            if ans.count(letter) > 1:
                isDouble = True
        
        if isDouble:
            ans = WordleSolver.getRandomAnswer()

global cnt
cnt = 0

currentWords = []

root = tk.Tk()
root.geometry("500x300")

letterVars = [[tk.StringVar() for i in range(length)] for j in range(6)]
answersVar = tk.StringVar()

def convToWord(vars):
    word = ""

    for i in range(length):
        word += vars[i].get()

    return word

def onEnterWordClicked(entries):
    global ans
    global cnt

    word = convToWord(letterVars[cnt])
    # print(f"{word} and {ans}")
    mask = WordleSolver.getColors(word, ans)
    for i in range(len(mask)):
        if mask[i] == "0":
            entries[cnt][i].config(bg="gray")
        elif mask[i] == "1":
            entries[cnt][i].config(bg="yellow")
        else:
            entries[cnt][i].config(bg="green")

    currentWords.append((word, mask))
    cnt += 1
    print(mask)


def onSearchClicked():    
    possibleWords = []
    if length == 6:
        possibleWords = WordleSolver.getSixLetterWords()
    else:
        possibleWords = WordleSolver.getPossibleWords()
    # if cnt > 2:
        possibleWords = WordleSolver.checkAnswers(possibleWords)
    
    words = []
    masks = []
    for word, mask in currentWords:
        words.append(word)
        masks.append(mask)
    
    info = WordleSolver.initInfo(words, masks)

    arr = WordleSolver.narrowDownCrude(possibleWords, info[0])


    print(arr)

    arr = WordleSolver.infoTheory(arr)
    # arr = WordleSolver.checkAnswers(arr)

    answersVar.set(f"The best word is: {arr[0]}")

def on_key(event):
    if str(event.char).isalnum():
        # Move focus to the next Entry widget
        event.widget.tk_focusNext().focus_set()

def onResetClicked(entries):
    global cnt
    for i in range(len(letterVars)):
        for j in range(len(letterVars[i])):
            letterVars[i][j].set("")
            entries[i][j].config(bg="white")
    
    createAnswer()
    currentWords.clear()
    cnt = 0
    

def initStuff():
    for widget in root.grid_slaves():
        widget.grid_forget()

    # inputWord = tk.Entry(root, textvariable=wordVar, width=50).grid(row=0, columnspan=3, column=0)
    inputLetters = [[tk.Entry(root, textvariable=letterVars[j][i], width=1) for i in range(length)] for j in range(6)]

    for i in range(6):
        for inputIndex in range(length):
            inputEntry = inputLetters[i][inputIndex]
            inputEntry.grid(row=i, column = inputIndex)
            inputEntry.bind('<Key>', on_key)

    wordButton = tk.Button(root, text="Enter this word.", command=lambda: onEnterWordClicked(inputLetters)).grid(row=0, column=length + 1)

    searchButton = tk.Button(root, text="Find Answers...", command=onSearchClicked).grid(row=1, column=length + 1)

    resetButton = tk.Button(root, text="Reset Words.", command=lambda: onResetClicked(inputLetters)).grid(row=2, column=length + 1)

    answers = tk.Label(root, textvariable=answersVar).grid(row=5, columnspan=2, column=length + 1)

initStuff()

createAnswer()
root.mainloop()

