from utilities import *

def CalculateDet():
    #get data from determinant program inputs
    global data
    global matrixSize
    global imatrix
    data = []
    imatrix = []
    rMatrixSize = matrixSize
    cMatrixSize = matrixSize
    for entry in entries:
        data.append(entry.get())
    for num in range(len(data)):
        try:
            data[num] = float(data[num])
        except ValueError:
            print('you gotta use numbers, silly!')
    for x in range(rMatrixSize):
        imatrix.append(data[cMatrixSize * x:cMatrixSize * (x + 1)])
    for x in range(cMatrixSize):
        if column(imatrix, x) != [0.0 for y in range(rMatrixSize)]:
            initpivotColumn = x
            break
        elif x == cMatrixSize - 1:
            roota.destroy()
            root = Tk()
            root.title('Determinant')
            answer = Label(root, text='Your determinant is', font=('Comic Sans MS', 36))
            ans2 = Label(root, text='0', font=('Comic Sans MS', 36))
            answer.pack()
            ans2.pack()
            root.mainloop()
    for x in range(rMatrixSize):
        potentialPivot = column(imatrix, initpivotColumn)[x]
        if potentialPivot != 0:
            initpivotRow = x
            break
    firstTopLeft = [initpivotRow, initpivotColumn]
    roota.destroy()
    rowReduce(imatrix, firstTopLeft)

    determinant = 1
    for x in range(len(imatrix)):
        determinant *= imatrix[x][x]

    root = Tk()
    root.title('Determinant')
    answer = Label(root, text='Your determinant is', font=('Comic Sans MS', 36))
    ans2 =  Label(root, text=int(determinant), font=('Comic Sans MS', 36))
    answer.pack()
    ans2.pack()
    root.mainloop()
