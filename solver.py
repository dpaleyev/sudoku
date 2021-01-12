def solve(grid):
    pos = grid.nextEmpty()
    if not pos:
        return True
    else:
        x, y = pos

    for i in range(1, 10):
        if grid.isCorrect(x, y, i):
            grid.grid[x][y] = i

            if solve(grid):
                return True

            grid.grid[x][y] = 0

    return False


def printSolution(grid):
    c = 1
    for i in range(9):
        for j in range(9):
            if grid.isChangable(i, j):
                print('Шаг:', c)
                c += 1
                print(i + 1, j + 1, grid.grid[i][j])
                for x in range(9):
                    if x != 0 and x % 3 == 0:
                        print('- - - - - - - - - - -')
                    for y in range(9):
                        if y != 0 and y % 3 == 0:
                            print('|', end = ' ')
                        if x <= i or (x == i and y <= i):
                            print("\033[31m{}".format(str(grid.grid[x][y])) if grid.isChangable(x,
                                                                                                y) else "\033[0m{}".format(
                                str(grid.grid[x][y])), end=' ')
                        else:
                            print("\033[31m{}".format('0') if grid.isChangable(x, y) else "\033[0m{}".format(
                                str(grid.grid[x][y])), end=' ')
                        print("\033[0m{}".format(''), end='')
                    print()
                print()