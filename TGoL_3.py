# The Game of Life [John Conway]

import os
import numpy
import time
import pandas as pd

os.chdir(os.path.split(__file__)[0])

# Cell Looks
inactiveCell = '⬜'
activeCell = '⬛'

matrixSizeIsValid = False
expectedReadFromArguments = 3

def matrixSizeAsParameter(disableMaxUpperLimit = False):
    global lowerSizeLimit, upperSizeLimit, matrixInitSize, defaultUpperSizeLimit, listFromFile, matrixSizeIsValid

    # TEMP
    # setupInitialMatrix()
    # TEMP
    # listFromFile=numpy.array(
    #     [
    #         [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True], [False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True], [True, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [True, True, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    #     ]
    # )

    # Matrix Dimensions
    lowerSizeLimit = max(numpy.size(listFromFile, 0),
                        numpy.size(listFromFile, 1)) + 3

    if not disableMaxUpperLimit:
        defaultUpperSizeLimit = 20
        if defaultUpperSizeLimit >= lowerSizeLimit + 5:
            upperSizeLimit = defaultUpperSizeLimit
        else:
            upperSizeLimit = lowerSizeLimit + 5
    else:
        upperSizeLimit = 10000

    # Initialising an empty matrix
    while not matrixSizeIsValid:
        matrixInitSize = input(f'Enter matrix size ({lowerSizeLimit} to {upperSizeLimit}): ')

        if matrixInitSize.isnumeric() and int(matrixInitSize) in range(lowerSizeLimit, upperSizeLimit+1):
            try:
                matrixSizeIsValid = True
                setupInitialMatrix(size=int(matrixInitSize))
            except Exception:
                raise
        else:
            try:
                if int(matrixInitSize) > upperSizeLimit:
                    print('Size too large')
                if int(matrixInitSize) < lowerSizeLimit:
                    print('Size too small')
                print(
                    f'Matrix size {matrixInitSize} not allowed, expected a value between {lowerSizeLimit} and {upperSizeLimit}')

            except ValueError:
                print('Expected int type value for matrix size')


def array_remove_surrounding_zeros(arrayInput):
    for _index, i in enumerate(arrayInput):
        if i.any():
            first_y = _index
            break

    for _index, i in enumerate(arrayInput[::-1]):
        if i.any():
            last_y = numpy.size(arrayInput, 0) - _index
            break

    for _index, i in enumerate(numpy.transpose(arrayInput)):
        if i.any():
            first_x = _index
            break

    for _index, i in enumerate(numpy.transpose(arrayInput)[::-1]):
        if i.any():
            last_x = numpy.size(arrayInput, 1) - _index
            break

    return arrayInput[first_y:last_y, first_x:last_x]

def setupInitialMatrix(size=10):
    global gameMatrix, matrixInitSize
    print(f'Initialising matrix of size {matrixInitSize} x {matrixInitSize}')
    gameMatrix = numpy.zeros([size, size], dtype='?') # Initialising a 2D boolean type numpy array

def readFromExcel(readFrom):
    global expectedReadFromArguments
    if len(readFrom) > expectedReadFromArguments:
        print(f'readFrom argument has more than {expectedReadFromArguments} arguments')
        raise SystemExit
        # return None

    if len(readFrom) < expectedReadFromArguments:
        print(f'readFrom argument has less than {expectedReadFromArguments} arguments')
        raise SystemExit
        # return None

    global excelFileContts, gameMatrix
    try:
        excelFileContts = pd.read_excel(readFrom[1], sheet_name=readFrom[2])
        excelFileContts = excelFileContts.fillna(False).replace('.', True)

        excelFileContts = excelFileContts.to_numpy(dtype='?')
        excelFileContts = array_remove_surrounding_zeros(excelFileContts)

        # gameMatrix = excelFileContts
        return excelFileContts
    
    except PermissionError:
        print(f'\nPermission error while opening excel file "{readFrom[1]}".\nCheck if this file is open in your system. If it is, close it and restart this program.\nExiting')
        raise SystemExit

def startMatrixSetup(readFrom, disableMaxUpperLimit = False):
    global listFromFile, matrixSizeIsValid, gameMatrix, matrixInitSize
    if readFrom[0] == 0:
        print('Input file type: "text"')
        try:
            with open(readFrom[1]) as f:
                rows = f.read().splitlines()
        except Exception:
            print(f'Exception in finding/reading file "{readFrom[1]}".')
            raise SystemExit

        # Initialising listFromFile with a temporary entry which will be deleted later
        listFromFile = numpy.array([2 for i in range(len(rows[0].split()))], dtype='i')

        try:
            for i in rows:
                if [j for j in i.split() if j in '0 1'.split()]:
                    listFromFile = numpy.vstack(
                        (listFromFile, numpy.array([int(j) for j in i.split()])))
                else:
                    print('Invalid integer(s) entered')
                    raise SystemExit

            listFromFile = listFromFile[1:]

        except Exception:
            print('Exception while processing file contents\n\n[Actual Error Message]:')
            raise

    elif readFrom[0] == 1:
        print('Input file type: "excel"')
        listFromFile = readFromExcel(readFrom)

    else:
        print(f'`readFrom` first value of ({readFrom[0]}) is invalid')
        raise SystemExit

    matrixSizeAsParameter(disableMaxUpperLimit=disableMaxUpperLimit)

    gameMatrix[
        int(numpy.size(gameMatrix, 0)/2 - numpy.size(listFromFile, 0)/2):
        int(numpy.size(gameMatrix, 0)/2 + numpy.size(listFromFile, 0)/2),

        int(numpy.size(gameMatrix, 1)/2 - numpy.size(listFromFile, 1)/2):
        int(numpy.size(gameMatrix, 1)/2 + numpy.size(listFromFile, 1)/2)
    ]=listFromFile

    # Save the original matrix for later use
    originalGameMatrix = gameMatrix


# [In anticlockwise direction starting from upperLeft]
def neighbours(cellX, cellY):
    if cellX >= len(gameMatrix) or cellY >= len(gameMatrix):
        return [None for i in range(6)]

    if cellX != 0:
        if cellY != 0:
            upperLeft = gameMatrix[cellX-1, cellY-1]
        else:
            upperLeft = None

        directUpper = gameMatrix[cellX-1, cellY]

        if cellY != len(gameMatrix)-1:
            upperRight = gameMatrix[cellX-1, cellY+1]
        else:
            upperRight = None
    else:
        upperRight, upperLeft, directUpper = None, None, None

    if cellX != len(gameMatrix)-1:
        if cellY != 0:
            lowerLeft = gameMatrix[cellX+1, cellY-1]
        else:
            lowerLeft = None

        directLower = gameMatrix[cellX+1, cellY]

        if cellY != len(gameMatrix)-1:
            lowerRight = gameMatrix[cellX+1, cellY+1]
        else:
            lowerRight = None
    else:
        lowerRight, lowerLeft, directLower = None, None, None

    if cellY != 0:
        directLeft = gameMatrix[cellX, cellY-1]
    else:
        directLeft = None
    if cellY != len(gameMatrix)-1:
        directRight = gameMatrix[cellX, cellY+1]
    else:
        directRight = None

    return [
        upperLeft,
        directUpper,
        upperRight,
        directRight,
        lowerRight,
        directLower,
        lowerLeft,
        directLeft
    ]

def checkNextState(cellX, cellY, verbose=False):
    activeNeighbourCount = neighbours(cellX, cellY).count(1)
    inactiveNeighbourCount = 8 - activeNeighbourCount

    if verbose:
        print(
            f'Cell is surrounded by exactly {activeNeighbourCount} active neighbours')

    if gameMatrix[cellX, cellY]:

        if verbose:
            print('The cell is active')
        if activeNeighbourCount in [2, 3]:
            nextState = 1

            if verbose:
                print('The cell will remain active in the next generation')
        else:
            nextState = 0

            if verbose:
                print('The cell will become inactive in the next generation')
    else:
        if verbose:
            print('The cell is inactive')

        if activeNeighbourCount == 3:
            nextState = 1

            if verbose:
                print('The cell will become active in the next generation')
        else:
            nextState = 0

            if verbose:
                print('The cell will remain inactive in the next generation')

    return nextState

def updateGameMatrix(verbose=False):
    global gameMatrix
    updatedMatrix = numpy.array([], dtype='i')
    for i in range(len(gameMatrix)):
        for j in range(len(gameMatrix)):
            updatedMatrix = numpy.append(
                updatedMatrix, checkNextState(i, j, verbose=verbose))
    gameMatrix = numpy.reshape(
        updatedMatrix, (len(gameMatrix), len(gameMatrix)))

def autoUpdateAndDisplay(printAll, overflow, goForever, delay=2000, verbose=False, disableOverflow = False):
    global iterations
    gameEndReason = None

    if not goForever:
        # Catches repeating cycles of any length
        savedMatrices = []

    matrixHasOccured = False
    iterations = 0

    # Check whether all elements are 0 or a matrix repeats or overflows
    while not (numpy.all((gameMatrix == 0)) or matrixHasOccured or iterations >= overflow):
        iterations += 1
        if disableOverflow:
            overflow = iterations + 1
            print('overflow:', overflow)
        if not goForever:
            savedMatrices.append(gameMatrix.tolist())
        updateGameMatrix(verbose=verbose)
        if not goForever:
            if gameMatrix.tolist() in savedMatrices:
                matrixHasOccured = True
        print(f'Iteration: {iterations}')

        # Method 1
        # print(tbl(gameMatrix, tablefmt='plain'))

        # Method 2
        for i in gameMatrix.tolist():
            for j in i:
                if j:
                    print(activeCell, end='')
                else:
                    print(inactiveCell, end='')
            print()

        time.sleep(delay/1000)
        if not printAll:
            os.system('cls' if os.name == 'nt' else 'clear')

    print(f'Iteration: {iterations}')
    for i in gameMatrix.tolist():
        for j in i:
            if j:
                print(activeCell, end='')
            else:
                print(inactiveCell, end='')
        print()

    if numpy.all((gameMatrix == 0)):
        gameEndReason = 'Matrix is empty'
    elif matrixHasOccured:
        gameEndReason = 'Matrix has occured once before'
    elif iterations >= overflow:
        gameEndReason = 'Reached overflow'

    print()
    print(f'Game ended in {iterations} iterations\nReason of game end: {gameEndReason}')

def playGame(
        fromSettings=(True, 'settings.json'),
        delay=2000,
        verbose=False,
        readFrom = (
            0,
            'my_game_of_life.txt',
            None
            ),
        overflow = 200,
        disableMaxUpperLimit = False,
        goForever = False,
        printAll = False,
        confirmStart = False,
        disableOverflow = False
    ):

    if fromSettings:
        import json
        try:
            with open(fromSettings[1], encoding='utf-8') as f:
                # Loading settings json file
                print('Loading settings json file')
                allSettings = json.load(f)
                
                # Importing settings
                readFrom=list(allSettings['readFrom'].values())
                goForever=allSettings['goForever']
                delay=allSettings['delay']
                printAll=allSettings['printAll']
                disableMaxUpperLimit=allSettings['disableMaxUpperLimit']
                overflow=allSettings['overflow']
                verbose=allSettings['verbose']
                confirmStart=allSettings['confirmStart']
                disableOverflow=allSettings['disableOverflow']

                print()
 
        except FileNotFoundError:
            print(f'File "{fromSettings[1]}" not found')
            raise SystemExit

    print("Setting up")
    startMatrixSetup(readFrom=readFrom, disableMaxUpperLimit=disableMaxUpperLimit)
    print("Initial Matrix")

    # Method 1
    # print(tbl(gameMatrix, tablefmt='plain'))

    # Method 2
    for i in gameMatrix.tolist():
        for j in i:
            if j:
                print(activeCell, end='')
            else:
                print(inactiveCell, end='')
        print()

    print()
    print('-'*80)
    if not confirmStart:
        input('Press [enter] to begin: ')

    time.sleep(delay/1000)
    if not printAll:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    autoUpdateAndDisplay(delay=delay, verbose=verbose, overflow=overflow, goForever=goForever, printAll=printAll, disableOverflow=disableOverflow)

# `readFrom` takes following values, with the following meanings:
# 
# +=============================+===================================================================+
# |            Value            |                               Meaning                             |
# +=============================+===================================================================+
# |  (0, <name of text file>)   |  Read from a text file path given in second item of tuple         |
# |  (1, <name of excel file>)  |  Read from an excel file with path given in second item of tuple  |
# +=============================+===================================================================+




# Play a game
if __name__ == '__main__':
    r'''
    playGame(
        readFrom=(
            1,
            'the_game_of_life.xlsx',
            'Gosper glider gun'
        ),
        fromSettings=(True, 'settings.json'),
        confirmStart=1, # Don't ask me for confirmation
        delay=10,  # No delay in printing scenes
        disableMaxUpperLimit=True,  # No upper limit to the size of matrix
        overflow=1000,  # Overflow after 1000 iterations
        goForever=1,  # Go until overflow
        # Do not print all iterations separately, only update the existing printed board.
        printAll=False
    )
    '''

    playGame(fromSettings=(True, 'settings.json'))

    # matrixSizeAsParameter()

# ToDo:
# Implement auto matrixSize as parameter and as setting
# Reason of game end
# Make xlsx presets for popular patterns
# Implement a settings.json file
