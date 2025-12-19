"""Класс игрового поля 5x5."""
import random
from typing import List, Tuple

# Импортируем константы из файла constants.py
from constants import BOARD_SIZE, PROBABILITY_2, PROBABILITY_4, INITIAL_TILES


class Board:
    """Игровое поле 5x5."""

    def __init__(self):
        """Создаёт новое поле с двумя начальными плитками."""
        self.size = BOARD_SIZE
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.max_tile = 0

        # Добавляем две начальные плитки
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> bool:
        """Добавляет случайную плитку в случайную пустую клетку."""
        empty_cells = self.get_empty_cells()

        if not empty_cells:
            return False

        row, col = random.choice(empty_cells)

        # Выбираем значение по вероятности
        value = 2 if random.random() < PROBABILITY_2 else 4
        self.grid[row][col] = value

        # Обновляем максимальную плитку
        if value > self.max_tile:
            self.max_tile = value

        return True

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Возвращает список координат пустых клеток."""
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    empty_cells.append((r, c))
        return empty_cells

    def move(self, direction: str) -> bool:
        """
        Двигает плитки в указанном направлении.
        Возвращает True, если поле изменилось.
        """
        if direction not in ["up", "down", "left", "right"]:
            return False

        # Сохраняем старое состояние для сравнения
        old_grid = [row[:] for row in self.grid]
        old_score = self.score

        if direction in ["left", "right"]:
            for row in range(self.size):
                self._process_row(row, direction)
        else:
            for col in range(self.size):
                self._process_col(col, direction)

        # Проверяем, изменилось ли что-то
        changed = (old_grid != self.grid) or (old_score != self.score)

        if changed:
            self.add_random_tile()
            # Обновляем максимальную плитку
            self.max_tile = max(max(row) for row in self.grid)

        return changed

    def _process_row(self, row: int, direction: str):
        """Обрабатывает строку при движении влево/вправо."""
        line = self.grid[row][:]

        # Для движения вправо переворачиваем строку
        if direction == "right":
            line = line[::-1]

        # Сдвигаем и объединяем
        new_line = self._shift_and_merge(line)

        # Возвращаем в исходный порядок
        if direction == "right":
            new_line = new_line[::-1]

        self.grid[row] = new_line

    def _process_col(self, col: int, direction: str):
        """Обрабатывает столбец при движении вверх/вниз."""
        # Получаем столбец
        line = [self.grid[r][col] for r in range(self.size)]

        # Для движения вниз переворачиваем
        if direction == "down":
            line = line[::-1]

        # Сдвигаем и объединяем
        new_line = self._shift_and_merge(line)

        # Возвращаем в исходный порядок
        if direction == "down":
            new_line = new_line[::-1]

        # Обновляем столбец
        for r in range(self.size):
            self.grid[r][col] = new_line[r]

    def _shift_and_merge(self, line: List[int]) -> List[int]:
        """Сдвигает и объединяет плитки в линии."""
        # Убираем нули
        non_zero = [x for x in line if x > 0]

        if not non_zero:
            return [0] * len(line)

        merged = []
        i = 0

        while i < len(non_zero):
            # Если можно объединить с следующей плиткой
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                new_value = non_zero[i] * 2
                merged.append(new_value)
                self.score += new_value  # Добавляем очки
                i += 2  # Пропускаем объединенную плитку
            else:
                merged.append(non_zero[i])
                i += 1

        # Заполняем нулями до нужной длины
        while len(merged) < len(line):
            merged.append(0)

        return merged

    def can_move(self) -> bool:
        """Проверяет, возможен ли хоть один ход."""
        # Проверяем пустые клетки
        if self.get_empty_cells():
            return True

        # Проверяем возможные слияния
        for r in range(self.size):
            for c in range(self.size):
                current = self.grid[r][c]
                if current == 0:
                    continue

                # Проверяем соседей
                if c + 1 < self.size and self.grid[r][c + 1] == current:
                    return True
                if r + 1 < self.size and self.grid[r + 1][c] == current:
                    return True

        return False

    def __str__(self) -> str:
        """Красивое отображение поля."""
        result = []
        for row in self.grid:
            line = []
            for cell in row:
                if cell == 0:
                    line.append("  .  ")
                else:
                    line.append(f"{cell:^5}")
            result.append(" ".join(line))
        return "\n".join(result)