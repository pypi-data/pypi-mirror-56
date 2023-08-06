from utilities import *

def CalculateSyst():
    #get data from determinant program inputs
    global data
    global rMatrixSize
    global cMatrixSize
    global imatrix
    data = []
    imatrix = []
    temp = []
    for entry in entries1:
        data.append(entry.get())
    for num in range(len(data)):
        try:
            data[num] = Decimal(data[num])
        except ValueError:
            print('you gotta use numbers, silly!')
    for x in range(rMatrixSize):
        for y in range(cMatrixSize):
            temp.append(data[rMatrixSize*y+x])
    for x in range(rMatrixSize):
        imatrix.append(temp[cMatrixSize * x:cMatrixSize * (x + 1)])
    for x in range(cMatrixSize):
        if column(imatrix, x) != [0.0 for y in range(rMatrixSize)]:
            initpivotColumn = x
            break
    for x in range(rMatrixSize):
        potentialPivot = column(imatrix, initpivotColumn)[x]
        if potentialPivot != 0:
            initpivotRow = x
            break
    firstTopLeft = [initpivotRow, initpivotColumn]
    rootb.destroy()
    rowReduce(imatrix, firstTopLeft)
    #check for no solution
    rMatrixSize = len(imatrix)
    cMatrixSize = len(imatrix[0])

    for x in range(rMatrixSize):
        for y in range(cMatrixSize):
            imatrix[x][y] = imatrix[x][y] / imatrix[x][x]
    for x in range(rMatrixSize - 1):
        for y in range(cMatrixSize - 2 - x):
            imatrix[rMatrixSize - 2 - y - x][cMatrixSize - 1] = \
                imatrix[rMatrixSize - 2 - y - x][cMatrixSize - 1] - (imatrix[rMatrixSize - 2 - y][cMatrixSize - 2 - x] * \
                                                                     imatrix[rMatrixSize - 1 - x][cMatrixSize - 1])
            imatrix[rMatrixSize - 2 - y - x][cMatrixSize - 2 - x] = 0
    for x in range(rMatrixSize):
        for y in range(cMatrixSize):
            imatrix[x][y] = imatrix[x][y] / imatrix[x][x]
            imatrix[x][y] = round(imatrix[x][y], 2)
    # for x in range(rMatrixSize):
    #     for y in range(cMatrixSize):
    #         imatrix[x][y] = round(imatrix[x][y], 2)
    root = Tk()
    root.title('System of Equations')
    answer = Label(root, text=imatrix, font=('Comic Sans MS', 36))
    answer.pack()
    root.mainloop()
