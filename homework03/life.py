import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
        grid: tp.Optional[Grid] = None,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        a = []
        if randomize == False:
            for i in range(0, self.rows):
                b = []
                for j in range(0, self.cols):
                    b.append(0)
                a.append(b)
        else:
            for i in range(0, self.rows):
                b = []
                for j in range(0, self.cols):
                    t = random.randint(0, 1)
                    b.append(t)
                a.append(b)
        return a
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        if cell[0] == 0:
            if cell[1] == 0:
                return [
                    self.curr_generation[0][1],
                    self.curr_generation[1][0],
                    self.curr_generation[1][1],
                ]
            elif cell[1] == self.cols - 1:
                return [
                    self.curr_generation[0][cell[1] - 1],
                    self.curr_generation[1][cell[1] - 1],
                    self.curr_generation[1][cell[1]],
                ]
            else:
                return [
                    self.curr_generation[0][cell[1] - 1],
                    self.curr_generation[1][cell[1] - 1],
                    self.curr_generation[1][cell[1]],
                    self.curr_generation[1][cell[1] + 1],
                    self.curr_generation[0][cell[1] + 1],
                ]
        elif cell[0] == self.rows - 1:
            if cell[1] == 0:
                return [
                    self.curr_generation[cell[0] - 1][0],
                    self.curr_generation[cell[0] - 1][1],
                    self.curr_generation[cell[0]][1],
                ]
            elif cell[1] == self.cols - 1:
                return [
                    self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0]][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1]],
                ]
            else:
                return [
                    self.curr_generation[cell[0]][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1]],
                    self.curr_generation[cell[0] - 1][cell[1] + 1],
                    self.curr_generation[cell[0]][cell[1] + 1],
                ]
        else:
            if cell[1] == 0:
                return [
                    self.curr_generation[cell[0] - 1][0],
                    self.curr_generation[cell[0] - 1][1],
                    self.curr_generation[cell[0]][1],
                    self.curr_generation[cell[0] + 1][1],
                    self.curr_generation[cell[0] + 1][0],
                ]
            elif cell[1] == self.cols - 1:
                return [
                    self.curr_generation[cell[0] - 1][cell[1]],
                    self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0]][cell[1] - 1],
                    self.curr_generation[cell[0] + 1][cell[1] - 1],
                    self.curr_generation[cell[0] + 1][cell[1]],
                ]
            else:
                return [
                    self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1]],
                    self.curr_generation[cell[0] - 1][cell[1] + 1],
                    self.curr_generation[cell[0]][cell[1] + 1],
                    self.curr_generation[cell[0] + 1][cell[1] + 1],
                    self.curr_generation[cell[0] + 1][cell[1]],
                    self.curr_generation[cell[0] + 1][cell[1] - 1],
                    self.curr_generation[cell[0]][cell[1] - 1],
                ]

    def get_next_generation(self) -> Grid:
        otvet = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.curr_generation[i][j])
            otvet.append(row)
        for i in range(self.rows):
            for j in range(self.cols):
                if (
                    sum(self.get_neighbours((i, j))) != 2 and sum(self.get_neighbours((i, j))) != 3
                ) and self.curr_generation[i][j] == 1:
                    otvet[i][j] = 0  # RIP dot of life(((
                elif sum(self.get_neighbours((i, j))) == 3 and self.curr_generation[i][j] == 0:
                    otvet[i][j] = 1  # Newbie is here!!!
        return otvet

    def step(self) -> None:
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:

        if self.max_generations is None:
            self.max_generations = 1
        if self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        if self.generations == 20:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f = open(filename, "r")
        h = sum(1 for line in f)
        f.close()
        f = open(filename, "r")
        s = f.readline()
        w = len(s)
        result = GameOfLife((w, h))
        a = []
        while s != "":
            b = []
            for i in s:
                b.append(ord(i) - ord("0"))
            a.append(b)
            s = f.readline()
        result.curr_generation = a
        return result

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for i in self.curr_generation:
            for c in i:
                f.write(str(c))
            f.write("\n")
            
