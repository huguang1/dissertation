from pyamaze import maze, agent, textLabel, COLOR


reword_direction = {
    ((1, 1), (1, 2)): 10,
    ((1, 2), (1, 3)): 10,
    ((1, 3), (1, 4)): 10,
    ((2, 1), (2, 2)): 7,
    ((2, 2), (2, 3)): 3,
    ((2, 3), (2, 4)): 9,
    ((3, 1), (3, 2)): 4,
    ((3, 2), (3, 3)): 5,
    ((3, 3), (3, 4)): 7,
    ((4, 1), (4, 2)): 10,
    ((4, 2), (4, 3)): 10,
    ((4, 3), (4, 4)): 10,
    ((1, 1), (2, 1)): 10,
    ((2, 1), (3, 1)): 10,
    ((3, 1), (4, 1)): 10,
    ((1, 2), (2, 2)): 2,
    ((2, 2), (3, 2)): 5,
    ((3, 2), (4, 2)): 8,
    ((1, 3), (2, 3)): 3,
    ((2, 3), (3, 3)): 6,
    ((3, 3), (4, 3)): 7,
    ((1, 4), (2, 4)): 10,
    ((2, 4), (3, 4)): 10,
    ((3, 4), (4, 4)): 10,
}


def get_reward(current_cell, next_cell):
    if (current_cell, next_cell) in reword_direction.keys():
        return reword_direction[(current_cell, next_cell)]
    elif (next_cell, current_cell) in reword_direction.keys():
        return reword_direction[(next_cell, current_cell)]
    else:
        return 0


####ValueIteration
def GetPath(m, D):
    cell = (m.rows, m.cols)
    Path = {}
    while cell != (1, 1):
        if D[cell] == 'E':
            Path[cell] = (cell[0], cell[1] + 1)
        elif D[cell] == 'W':
            Path[cell] = (cell[0], cell[1] - 1)
        elif D[cell] == 'N':
            Path[cell] = (cell[0] - 1, cell[1])
        else:
            Path[cell] = (cell[0] + 1, cell[1])
        cell = Path[cell]
    return Path


def ValueIteration(m):
    V = {cell: float(0) for cell in m.grid}
    V[(1, 1)] = 100
    D = {cell: "" for cell in m.grid}
    Noise = 0.2
    Discount = 0.9

    def NextCell(d, a):
        if (d == 'E' and a == 'R') or (d == 'S' and a == 'S') or (d == 'W' and a == 'L'):
            nextCell = (currCell[0] + 1, currCell[1])
        elif (d == 'E' and a == 'L') or (d == 'W' and a == 'R') or (d == 'N' and a == 'S'):
            nextCell = (currCell[0] - 1, currCell[1])
        elif (d == 'S' and a == 'R') or (d == 'W' and a == 'S') or (d == 'N' and a == 'L'):
            nextCell = (currCell[0], currCell[1] - 1)
        else:
            nextCell = (currCell[0], currCell[1] + 1)
        if nextCell[0] < 1 or nextCell[0] > 4 or nextCell[1] < 1 or nextCell[1] > 4:
            nextCell = currCell
        return nextCell
    count = 0

    while True:
        oldV = V.copy()
        for currCell in m.grid:
            if currCell == (1, 1):
                continue
            Q = {}
            ETmp = WTmp = NTmp = STmp = 0
            for a in 'ESNW':
                if a == 'E':
                    nextCell = NextCell(a, 'S')
                    aa = get_reward(currCell, nextCell)
                    ETmp = (1 - Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'L')
                    aa = get_reward(currCell, nextCell)
                    NTmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'R')
                    aa = get_reward(currCell, nextCell)
                    STmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                elif a == 'S':
                    nextCell = NextCell(a, 'S')
                    aa = get_reward(currCell, nextCell)
                    ETmp = (1 - Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'R')
                    aa = get_reward(currCell, nextCell)
                    NTmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'L')
                    aa = get_reward(currCell, nextCell)
                    STmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                elif a == 'N':
                    nextCell = NextCell(a, 'S')
                    aa = get_reward(currCell, nextCell)
                    ETmp = (1 - Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'L')
                    aa = get_reward(currCell, nextCell)
                    NTmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'R')
                    aa = get_reward(currCell, nextCell)
                    STmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                else:
                    nextCell = NextCell(a, 'S')
                    aa = get_reward(currCell, nextCell)
                    ETmp = (1 - Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'R')
                    aa = get_reward(currCell, nextCell)
                    NTmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                    nextCell = NextCell(a, 'L')
                    aa = get_reward(currCell, nextCell)
                    STmp = (0.5 * Noise) * (-1 * get_reward(currCell, nextCell) + oldV[nextCell] * Discount)
                Q[a] = ETmp + WTmp + NTmp + STmp
                count = count + 1

            QMax = max(Q, key=Q.get)
            V[currCell] = Q[QMax]
            D[currCell] = QMax
        if all(oldV[cell] == V[cell] for cell in m.grid):
            break
    print(D)
    print(V)
    path = GetPath(m, D)
    return V, D, path, count


if __name__ == '__main__':
    algrithm = "ValueIteration"
    # MyMaze = maze(4, 4)
    # MyMaze.CreateMaze(loadMaze="maze4x4.csv", theme=COLOR.light)
    MyMaze = maze(4, 4)
    MyMaze.CreateMaze(loadMaze="maze4.csv", theme=COLOR.light)
    # MyMaze=maze(20,20)
    # MyMaze.CreateMaze(loadMaze="maze20.csv",theme=COLOR.light)
    # MyMaze=maze(30,30)·
    # MyMaze.CreateMaze(loadMaze="maze30x30.csv",theme=COLOR.light)
    V, D, fwdPath, count = ValueIteration(MyMaze)
    print(V)
    print(D)
    print(count)
    a = agent(MyMaze, footprints=True, color=COLOR.red, shape='arrow', filled=False)
    textLabel(MyMaze, algrithm + ' Path Length', len(fwdPath) + 1)
    # T = timeit(stmt='ValueIteration(MyMaze)', number=10, globals=globals())
    # textLabel(MyMaze, 'Time', T)
    textLabel(MyMaze, "Calculation times", count)
    print(algrithm + ' Path Length', len(fwdPath) + 1)
    # print(algrithm + ' Time', T)
    print("Calculation times", count)
    MyMaze.tracePath({a: fwdPath}, delay=100)
    MyMaze.run()
