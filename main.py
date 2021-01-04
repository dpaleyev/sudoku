import os
import pickle

from player_game import Game, Grid
from solver import solve, printSolution


def user_game():
    flag = False
    if os.path.exists('saving'):
        r = input('Хотите продолжить игру? Да/Нет: ')
        if r.strip().lower() == 'да':
            flag = True
    if flag:
        infile = open('saving', 'rb')
        game = pickle.load(infile)
        infile.close()
        os.remove('saving')
    else:
        num = int(input('Введите количество заполненных клеток: '))
        game = Game(num)
    os.system('cls||clear')
    while not game.isCompleted():
        game.showGrid()
        while not game.makeMove():
            pass
        os.system('cls||clear')

    print('Вы победили!!!')
    s = input('Хотите сыграть ещё? Да/Нет: ')
    if s.strip().lower() != 'да':
        exit()
    else:
        os.system('cls||clear')


def comp_game():
    print('Введите судоку:')
    sudoku = []
    for i in range(9):
        sudoku.append([int(i) for i in input().split()])
    g = Grid(arr=sudoku)
    if solve(g):
        printSolution(g)
    else:
        print('Ваше судоку не имеет решения :(')

    s = input('Хотите сыграть ещё? Да/Нет: ')
    if s.strip().lower() != 'да':
        exit()
    else:
        os.system('cls||clear')


if __name__ == '__main__':
    sel_type = None
    while True:
        sel_type = input('Выберите тип игры:\n 1. Решать судоку\n 2. Игра против компьютера\nВаш выбор: ')
        if sel_type == '1':
            user_game()
        elif sel_type == '2':
            comp_game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
