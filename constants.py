"""Константы игры 4096."""

# Размер игрового поля
BOARD_SIZE = 5

# Цель игры
WIN_VALUE = 4096

# Базовые значения плиток
INITIAL_TILES = [2, 4]

# Вероятности появления плиток
PROBABILITY_2 = 0.9  # 90% шанс появления двойки
PROBABILITY_4 = 0.1  # 10% шанс появления четверки

# Управление
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

DIRECTION_KEYS = {
    "w": UP,
    "s": DOWN,
    "a": LEFT,
    "d": RIGHT,
    "ц": UP,
    "ы": DOWN,
    "ф": LEFT,
    "в": RIGHT,
}
