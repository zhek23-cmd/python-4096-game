"""Класс управления игровым процессом."""
from board import Board
from constants import WIN_VALUE, DIRECTION_KEYS


class Game:
    """Управляет всей игрой: поле, счет."""
    
    def __init__(self):
        """Инициализация новой игры."""
        self.board = Board()
        self.game_over = False
        self.won = False
        self.high_score = 0
        
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
        
        # Проверяем, не закончилась ли игра
        if not self.board.can_move():
            self.game_over = True
            self.save_high_score()
        
        return True
    
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
