from pyamaze import maze, agent, textLabel, COLOR


reword_direction = {
    ((1, 1), (1, 2)): 10,
    ((1, 2), (2, 1)): 10,
    ((1, 1), (2, 1)): 30,
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
    V = {(): float(0)}
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
    V, D, fwdPath, count = ValueIteration(MyMaze)
    print(V)
    print(D)
    print(count)
    a = agent(MyMaze, footprints=True, color=COLOR.red, shape='arrow', filled=False)
    textLabel(MyMaze, algrithm + ' Path Length', len(fwdPath) + 1)
    textLabel(MyMaze, "Calculation times", count)
    print(algrithm + ' Path Length', len(fwdPath) + 1)
    print("Calculation times", count)
    MyMaze.tracePath({a: fwdPath}, delay=100)
    MyMaze.run()
