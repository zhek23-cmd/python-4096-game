"""Класс управления игровым процессом."""
import random
from board import Board
from constants import WIN_VALUE, BONUS_VALUES, BONUS_SYMBOLS, BONUS_DESCRIPTIONS, DIRECTION_KEYS, RECORD_THRESHOLDS


class Game:
    """Управляет всей игрой: поле, счет, бонусы."""

    def __init__(self):
        """Инициализация новой игры."""
        self.board = Board()
        self.game_over = False
        self.won = False
        self.high_score = 0  # Лучший счет за сессию
        self.record_values = set()  # Какие рекордные значения уже были

        # Загружаем лучший счет из файла (если есть)
        self.load_high_score()

    def load_high_score(self):
        """Загружает лучший счет из файла."""
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        """Сохраняет лучший счет в файл."""
        if self.board.score > self.high_score:
            self.high_score = self.board.score
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))

    def move(self, direction: str) -> bool:
        """
        Выполняет ход в указанном направлении.

        Returns:
            True, если ход был выполнен успешно
            False, если игра окончена или ход невозможен
        """
        if self.game_over:
            return False

        # Пробуем сделать ход
        moved = self.board.move(direction)

        if not moved:
            # Ход не изменил поле
            if not self.board.can_move():
                self.game_over = True
                self.save_high_score()
            return False

        # Проверяем победу
        if self.board.max_tile >= WIN_VALUE and not self.won:
            self.won = True
            print(f"\n🎉 ПОБЕДА! Вы достигли {WIN_VALUE}!")

        # Проверяем, достигли ли нового рекордного значения для бонуса
        self._check_for_bonus()

        # Проверяем, не закончилась ли игра
        if not self.board.can_move():
            self.game_over = True
            self.save_high_score()

        return True

    def _check_for_bonus(self):
        """Проверяет, не достигли ли мы нового рекордного значения."""
        current_max = self.board.max_tile

        # Новые рекордные значения: 64, 128, 256, 512, 1024, 2048, 4096
        record_thresholds = [64, 128, 256, 512, 1024, 2048, 4096]

        for threshold in record_thresholds:
            if current_max >= threshold and threshold not in self.record_values:
                # Получили новый рекорд!
                self.record_values.add(threshold)
                self._spawn_bonus(threshold)
                break

    def _spawn_bonus(self, value: int):
        """Создает бонусную плитку при достижении нового рекорда."""
        # Сначала найдем все пустые клетки
        empty_cells = self.board.get_empty_cells()

        if not empty_cells:
            print(f"\n🎁 Достигнут рекорд {value}! Но нет места для бонуса.")
            return

        # Выбираем случайную пустую клетку
        row, col = random.choice(empty_cells)

        # Случайно выбираем тип бонуса
        bonus_type = random.choice(list(BONUS_VALUES.keys()))
        bonus_value = BONUS_VALUES[bonus_type]
        bonus_symbol = BONUS_SYMBOLS[bonus_value]

        # Помещаем бонус на поле
        self.board.grid[row][col] = bonus_value

        print(f"\n🎁 Достигнут рекорд {value}! Появилась бонусная плитка: {bonus_symbol}")
        print(f"   {BONUS_DESCRIPTIONS[bonus_value]}")

    def get_state(self) -> dict:
        """Возвращает текущее состояние игры."""
        return {
            'grid': self.board.grid,
            'score': self.board.score,
            'max_tile': self.board.max_tile,
            'game_over': self.game_over,
            'won': self.won,
            'high_score': self.high_score,
            'board_size': self.board.size
        }

    def get_instructions(self) -> str:
        """Возвращает инструкции по управлению."""
        return (
            "Управление:\n"
            "  w / ↑  - вверх\n"
            "  a / ←  - влево\n"
            "  s / ↓  - вниз\n"
            "  d / →  - вправо\n"
            "  q      - выход\n"
            "  r      - новая игра"
        )