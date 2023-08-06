
def column(matrix, columnNo):
    return [matrix[x][columnNo] for x in range(len(matrix))]

def rowReduce(matrix, topLeft):
    #recalculate rmatrixsize and cmatrixsize
    rMatrixSize = len(matrix)
    cMatrixSize = len(matrix[0])
    if rMatrixSize != 1:
        #find pivot
        for x in range(cMatrixSize):
            if column(matrix, x) != [0.0 for y in range(rMatrixSize)]:
                pivotColumn = x
                break
            elif x == cMatrixSize - 1:
                return
        for x in range(rMatrixSize):
            potentialPivot = column(matrix, pivotColumn)[x]
            if potentialPivot != 0:
                pivotRow = x
                break
        if pivotRow+1 == rMatrixSize:
            return
        #create zeros below pivot
        for y in range(rMatrixSize-1):
            scalaR1R2 = matrix[pivotRow+y+1][pivotColumn]/matrix[pivotRow][pivotColumn]
            scaledR1 = [scalaR1R2*matrix[0][x] for x in range(cMatrixSize)]
            matrix[y+1] = [matrix[y+1][x]-scaledR1[x] for x in range(cMatrixSize)]
        #cover row containing pivot, and repeat
        for x in range(rMatrixSize):
            for y in range(cMatrixSize):
                # print(matrix[x][y])
                # print(imatrix[topLeft[0]+x][topLeft[1]+y])
                imatrix[topLeft[0]+x][topLeft[1]+y] = matrix[x][y]
        topLeft = [topLeft[0] + 1 + pivotRow, topLeft[1] + 1 + pivotColumn]
        matrix = matrix[1:]
        matrix = [matrix[x][1:] for x in range(rMatrixSize-1)]
        rowReduce(matrix, topLeft)
    else:
        return
