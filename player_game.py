import pickle
import random


class Grid:
    default_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                    [4, 5, 6, 7, 8, 9, 1, 2, 3],
                    [7, 8, 9, 1, 2, 3, 4, 5, 6],
                    [2, 3, 4, 5, 6, 7, 8, 9, 1],
                    [5, 6, 7, 8, 9, 1, 2, 3, 4],
                    [8, 9, 1, 2, 3, 4, 5, 6, 7],
                    [3, 4, 5, 6, 7, 8, 9, 1, 2],
                    [6, 7, 8, 9, 1, 2, 3, 4, 5],
                    [9, 1, 2, 3, 4, 5, 6, 7, 8]]

    def __init__(self, arr=None, n=None, flag_random=False):
        self.locked_cells = []
        if flag_random:
            self.fill_randomly(n)
        else:
            self.grid = arr

        for i in range(9):
            l = []
            for j in range(9):
                l.append(0 if self.grid[i][j] == 0 else 1)
            self.locked_cells.append(l)

    def nextEmpty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def isCorrect(self, x, y, num):
        for i in range(9):
            if self.grid[i][y] == num:
                return False
            if self.grid[x][i] == num:
                return False

        area_x = x // 3
        area_y = y // 3

        for dx in range(3):
            for dy in range(3):
                if self.grid[area_x * 3 + dx][area_y * 3 + dy] == num:
                    return False

        return True



    def fill_randomly(self, n):
        order = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(order)
        self.grid = []
        for i in range(9):
            l = []
            for j in range(9):
                l.append(order[Grid.default_grid[i][j] - 1])
            self.grid.append(l)
        for i in range(12):
            Grid.swap_rand_rows(self)
        for i in range(81 - n):
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            while self.grid[x][y] == 0:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
            self.grid[x][y] = 0

    def isChangable(self, x, y):
        return self.locked_cells[x][y] == 0

    def transpose(self):
        self.grid = list(map(list, zip(*self.grid)))

    def swap_rand_rows(self):
        t = random.randint(0, 1)
        if t == 1:
            Grid.transpose(self)

        area = random.randint(0, 2)
        row1 = random.randint(0, 2)
        row2 = random.randint(0, 2)

        self.grid[area * 3 + row1], self.grid[area * 3 + row2] = self.grid[area * 3 + row2], self.grid[area * 3 + row1]

        if t == 1:
            Grid.transpose(self)
    
    def __str__(self):
        return '\n'.join(' '.join(str(j) for j in i)for i in self.grid)


class Game:
    def __init__(self, n):
        self.grid = Grid(n=n, flag_random=True)

    def showGrid(self):
        for i in range(9):
            for j in range(9):
                print("\033[31m{}".format(str(self.grid.grid[i][j])) if self.grid.isChangable(i,
                                                                                              j) else "\033[30m{}".format(
                    str(self.grid.grid[i][j])), end=' ')
            print()

    def isCompleted(self):
        for i in range(9):
            if not all(self.grid.grid[i]):
                return False

        for i in range(9):
            s = set(self.grid.grid[i])
            if not len(s) == 9:
                return False

        for i in range(9):
            s = set()
            for j in range(9):
                s.add(self.grid.grid[j][i])
            if not len(s) == 9:
                return False

        for i in range(3):
            for j in range(3):
                s = set()
                x = 3 * i
                y = 3 * j
                for dx in range(3):
                    for dy in range(3):
                        s.add(self.grid.grid[x + dx][y + dy])
                if not len(s) == 9:
                    return False

        return True

    def makeMove(self):
        print("\033[30m{}".format(
            'Сделайте ход в формате \'[строка] [столбец] [число]\', либо завершите игру, написав \'выйти\''))
        resp = input('Ваш ход: ').split()
        if resp[0].lower() == 'выйти':
            s_resp = input('Хотите сохранить прогресс? Да/Нет: ')
            if s_resp.strip().lower() == 'да':
                filename = 'saving'
                outfile = open(filename, 'wb')
                pickle.dump(self, outfile)
                outfile.close()
            exit()

        if len(resp) == 3 and resp[0].isdigit() and 1 <= int(resp[0]) <= 9 and resp[1].isdigit() and 1 <= int(
                resp[1]) <= 9 and resp[2].isdigit() and 1 <= int(resp[2]) <= 9:
            x, y, number = [int(i) for i in resp]
        else:
            print('Неправильный запрос, попробуйте ещё раз')
            return False

        if self.grid.isChangable(x - 1, y - 1):
            self.grid.grid[x - 1][y - 1] = number
            return True
        else:
            print('Эта клетка является частью головолмки, Вы не можете изменить её')
            return False
