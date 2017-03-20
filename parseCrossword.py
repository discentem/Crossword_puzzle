import time
def partOfPuzzle(char):
    '''
    Returns True if char, presumably the first char of a line of input,
    is part of a puzzle. 
    '''
    try:
        char = char.lower()
        return True
    except:
        return ord(letter) == 42

def dimRead(char):
    '''
    Returns true if char, presumably the first char in a line of input,
    is part of dimension information. 
    '''
    return ord(char) >= 49 and ord(char) <= 58

def storeCrosswords(file):
    '''
    Parses a text file, representing n solved crosswords,
    into a 3D list.
    '''
    puzzles = []
    cols = 0
    rows = 0
    lineCount = 0
    selected = -1
    for line in file:
        f = line[0]
        if dimRead(f) == True:
            cols = int(line[0])
            rows = int(line[2]) 
            list = [[0 for x in range(rows)] for x in range(cols)]
            puzzles.append(list)
            selected+=1
            lineCount=-1
            continue
        elif partOfPuzzle(f) == True or f == "\n":
            lineCount+=1
            for char in range(len(line)):
                try:
                    puzzles[selected][lineCount][char] = line[char]
                except:
                    continue
    return puzzles
           
def emp(str):
    '''
    Returns True if a str is empty. 
    '''
    return str == ""

def numbering(puzzle):
    '''
    Creates a number grid for a crossword puzzle,
    based on the following rules:

    White squares with black squares (represented by "*") immediately to the left or
    above them are “eligible” to be numbered. White squares with no squares either
    immediately to the left or above are also “eligible” to be numbered.
    No other squares are numbered. All of the squares on the first row are numbered.
    '''
    list = [["__" for x in range(len(puzzle[0]))] for x in range(len(puzzle))]
    count = 1
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == "*":
                list[i][j] = "**"
            elif puzzle[i][j-1] == "*" or puzzle[i-1][j] == "*" or i == 0 or j == 0:
                if len(str(count)) == 1:
                    list[i][j] = "0" + str(count)
                else:
                    list[i][j] = str(count)
                count+=1
    return list       

def parseAcross(puzzle, eli):
    '''
    Returns a list of the across words of a crossword puzzle,
    numbered correctly. 
    '''
    acrossList = []
    first = True
    word = ""
    number = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            chr = puzzle[i][j]
            if first and eli[i][j] != "**":
                number = int(eli[i][j])
                first = False
            if chr == "*":
                if(not(emp(word))):
                    acrossList.append((number,word))
                    word = ""
                    first = True
                    continue
            else:
                word+=chr
        if not(emp(word)):
            acrossList.append((number, word))
            word = ""
            first = True
    return acrossList #sorted(acrossList)

def parseDown(puzzle, eli):
    '''
    Returns a list of the across words of a crossword puzzle,
    numbered correctly.
    '''
    downList = []
    first = True
    word = ""
    number = 0
    j = 0
    while(True):
        number+=1
        if j <= len(puzzle[0])-1:
            for i in range(len(puzzle)):
                chr = puzzle[i][j]
                if first and eli[i][j] != "**":
                    number = int(eli[i][j])
                    first = False
                if chr == "*":
                    if not(emp(word)):
                        downList.append((number,word))
                    word = ""
                    first = True
                    continue
                
                word+=chr
            if not(emp(word)):
                downList.append((number,word))
                word = ""
                first = True
            j+=1
        else:
            break
    return sorted(downList)

def saveResults(a, string):
    file = open("crosswordOutput.txt", "a")
    list = []
    list.append(string)
    for item in a:
        num = item[0]
        if num >= 10:
            list.append("\n" + " " + str(num) + "." + item[1])
        else:
            list.append("\n" + "  " + str(num) + "." + item[1])
    for item in list:
        file.write(item)
    file.write("\n")
    file.close()

def sep():
    '''
    Prints "---", used to seperate output data. 
    '''
    print("---")

def display(puzzles):
    '''
    Displays the 2d matrix for each crossword. 
    '''
    for puzzle in puzzles:
        for line in puzzle:
            print(line)
        sep()
            
def main():
    '''
    Stores puzzles in 3d array, displays/prints each layer, and prints the across/down
    with the correct numbers by running relevant functions. 
    '''
    tic = time.time()
    file = open("crosswordInput.txt", "r")
    puzzles = storeCrosswords(file)
    file.close()
    file = open("crosswordOutput.txt", "w")
    file.write("")
    file.close()

    for puzzle in puzzles:
        file = open("crosswordOutput.txt", "a")
        if puzzles.index(puzzle) == 0:
            file.write("puzzle #" + str(puzzles.index(puzzle)+1) + "\n")
        else:
            file.write("\npuzzle #" + str(puzzles.index(puzzle)+1) + "\n")
        file.close()
        grid = numbering(puzzle) #numbering system
        #for line in grid:
            #print(line)
        across = parseAcross(puzzle, grid) #list of across words
        across = saveResults(across, "Across") #saves to ouput txt file
        down = parseDown(puzzle, grid) #list of down words
        #print(down)
        down = saveResults(down, "Down") #save to output txt file
    toc = time.time() - tic
    file = open("crosswordOutput.txt", "r")
    for line in file:
        print(line, end = '')
    print("Completed in:" + str(toc))   

main()
        
    
    
