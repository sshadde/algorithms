"""Практические задачи с применением рекурсии."""

import os
from typing import List, Optional, Any


def binary_search(arr: List[Any], target: Any, low: int = 0,
                  high: Optional[int] = None) -> Optional[int]:
    """
    Рекурсивный бинарный поиск элемента в отсортированном массиве.

    Args:
        arr: Отсортированный массив
        target: Искомый элемент
        low: Нижняя граница поиска
        high: Верхняя граница поиска
    Returns:
        Индекс элемента или None, если не найден
    """
    if high is None:
        high = len(arr) - 1

    if low > high:
        return None

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid

    if arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)
# Временная сложность: O(log n)
# Глубина рекурсии: O(log n)


def file_system_walk(path: str, level: int = 0,
                     max_depth: Optional[int] = None) -> None:
    """
    Рекурсивный обход файловой системы с выводом дерева каталогов.

    Args:
        path: Начальный путь для обхода
        level: Текущий уровень вложенности
        max_depth: Максимальная глубина рекурсии
    """
    if max_depth is not None and level > max_depth:
        return

    try:
        with os.scandir(path) as entries:
            for entry in entries:
                indent = '  ' * level
                if entry.is_dir():
                    print(f'{indent}DIR {entry.name}/')
                    file_system_walk(entry.path, level + 1, max_depth)
                else:
                    print(f'{indent}FILE {entry.name}')
    except PermissionError:
        print(f'{indent}Доступ запрещен: {path}')
# Временная сложность: O(n), где n — количество файлов/папок
# Глубина рекурсии: равна глубине вложенности директорий


def hanoi(n: int, source: str = 'A', secondary: str = 'B',
          target: str = 'C', moves: int = 0) -> int:
    """
    Рекурсивное решение задачи Ханойских башен.

    Args:
        source: Начальный стержень
        secondary: Вспомогательный стержень
        target: Требуемый стержень
    Returns:
        moves: Количество ходов
    """
    if n == 1:
        moves += 1
        print(f'Переместить диск 1 с {source} на {target}')
        return moves

    moves = hanoi(n - 1, source, target, secondary, moves)
    moves += 1
    print(f'Переместить диск {n} с {source} на {target}')
    moves = hanoi(n - 1, secondary, source, target, moves)
    return moves
# Временная сложность: O(2^n)
# Глубина рекурсии: O(n).


def measure_max_recursion_depth() -> int:
    """
    Измерение максимальной глубины рекурсии для обхода файловой системы.

    Returns:
        Максимальная глубина рекурсии
    """
    def get_depth(path: str, current_depth: int) -> int:
        """
        Функция для нахождения глубины рекурсии.

        Args:
            path: Начальный путь
            current_depth: Текущая глубина
        Returns:
            Возвращает текущую глубину рекурсии
        """
        try:
            max_depth = current_depth
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        depth = get_depth(entry.path, current_depth + 1)
                        max_depth = max(max_depth, depth)
            return max_depth
        except (PermissionError, OSError):
            return current_depth

    start_path = '.'
    return get_depth(start_path, 0)
# Временная сложность: O(n)
# Глубина рекурсии: максимальная глубина вложенности папок


if __name__ == '__main__':
    print('=== Бинарный поиск ===')
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 11
    index = binary_search(sorted_array, target)
    print(f'Массив: {sorted_array}')
    print(f'Элемент {target} найден по индексу: {index}')

    print('\n=== Обход файловой системы ===')
    file_system_walk('./lab03/', max_depth=3)

    print('\n=== Ханойские башни ===')
    print('Решение для 4 дисков:')
    moves = hanoi(4)
    print(f'Всего ходов: {moves}')

    print('\n=== Измерение глубины рекурсии ===')
    max_depth = measure_max_recursion_depth()
    print(f'Максимальная глубина рекурсии: {max_depth}')
