"""Главный файл игры 4096."""
import os
import sys
import msvcrt  # Для Windows - чтение клавиш без нажатия Enter
from game import Game
from constants import DIRECTION_KEYS, COLORS, USE_COLORS


def clear_screen():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')


def colorize(text, value):
    """Добавляет цвет к тексту в зависимости от значения."""
    if not USE_COLORS:
        return text

    if value in COLORS:
        return f"{COLORS[value]}{text}{COLORS['reset']}"

    # Для больших значений используем цвет из ближайшего меньшего
    for threshold in [4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2]:
        if value >= threshold:
            return f"{COLORS[threshold]}{text}{COLORS['reset']}"

    return text


def display_grid(grid):
    """Выводит игровое поле в консоли."""
    print("\n" + "═" * 45)
    print(" " * 15 + "ИГРОВОЕ ПОЛЕ")
    print("═" * 45)
    
    for row in grid:
        display_row = []
        for cell in row:
            if cell == 0:
                display_row.append(colorize("  .  ", 0))
            else:
                text = f"{cell:^5}"
                display_row.append(colorize(text, cell))
        print(" ".join(display_row))
    print("═" * 45)


def get_key():
    """Читает одну клавишу без нажатия Enter."""
    try:
        # Пробуем прочитать одну клавишу
        key = msvcrt.getch().decode('utf-8').lower()

        # Проверяем специальные клавиши (стрелки)
        if key == '\xe0':  # Код стрелки
            second_char = msvcrt.getch().decode('utf-8')
            arrow_keys = {
                'H': 'up',
                'P': 'down',
                'K': 'left',
                'M': 'right'
            }
            if second_char in arrow_keys:
                return arrow_keys[second_char]
        return key
    except:
        # Если не получилось, используем обычный input
        return input().strip().lower()


def print_header():
    """Печатает заголовок игры."""
    print("═" * 50)
    print(" " * 20 + "ИГРА 4096")
    print("═" * 50)
    print("Цель: Собирайте плитки, чтобы достичь 4096!")
    print("Бонусы: При достижении 64, 128, 256... появляются специальные плитки")
    print("═" * 50)


def print_game_info(state):
    """Печатает информацию о текущей игре."""
    print(f"\n🏆 Счет: {state['score']}")
    print(f"👑 Рекорд: {state['high_score']}")
    print(f"📊 Максимальная плитка: {state['max_tile']}")

    if state['won']:
        print("🎉 ПОЗДРАВЛЯЕМ! Вы достигли 4096!")
    elif state['game_over']:
        print("💀 ИГРА ОКОНЧЕНА! Нет возможных ходов.")


def print_controls():
    """Печатает информацию об управлении."""
    print("\n" + "─" * 50)
    print("Управление:")
    print("  W / ↑  - Движение вверх")
    print("  S / ↓  - Движение вниз")
    print("  A / ←  - Движение влево")
    print("  D / →  - Движение вправо")
    print("  R      - Новая игра")
    print("  Q      - Выход")
    print("─" * 50)


def main():
    """Основной игровой цикл."""
    game = Game()

    while True:
        clear_screen()
        print_header()

        # Получаем состояние игры
        state = game.get_state()

        # Выводим информацию об игре
        print_game_info(state)

        # Выводим поле
        display_grid(state['grid'])

        # Выводим управление
        print_controls()

        # Проверяем состояние игры
        if state['game_over']:
            print("\n" + "═" * 50)
            restart = input("\nСыграть еще раз? (Y/N): ").strip().lower()
            if restart == 'y':
                game = Game()
                continue
            else:
                print("\nСпасибо за игру! До свидания!")
                break

        # Получаем ввод пользователя
        print("\nВаш ход (W/A/S/D или стрелки): ", end='', flush=True)
        command = get_key()

        print(command)  # Показываем, что нажали

        if command == 'q':
            print("\nСпасибо за игру! Сохраняем рекорд...")
            game.save_high_score()
            break

        if command == 'r':
            print("\nНачинаем новую игру...")
            input("Нажмите Enter чтобы продолжить...")
            game = Game()
            continue

        # Обрабатываем движение
        if command in DIRECTION_KEYS:
            direction = DIRECTION_KEYS[command]
            if not game.move(direction):
                print("Ход невозможен! Попробуйте другое направление.")
                input("Нажмите Enter чтобы продолжить...")
        else:
            print(f"Неизвестная команда: '{command}'")
            input("Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        input("Нажмите Enter чтобы выйти...")
