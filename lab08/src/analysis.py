"""Сравнение дробного жадного рюкзака и замеры Хаффмана."""
from typing import List, Tuple
import time
from greedy_algorithms import fractional_knapsack


def brute_force_01(values: List[float], weights: List[float],
                   capacity: int) -> Tuple[float, List[int]]:
    """Полный перебор всех комбинаций для 0-1 рюкзака.

    Работает для маленьких n (<= 20).

    Возвращает (max_value, taken_vector).
    """
    n = len(values)
    best_value = 0.0
    best_choice: List[int] = [0] * n

    for mask in range(1 << n):
        total_w = 0.0
        total_v = 0.0
        choice = [0] * n
        for i in range(n):
            if (mask >> i) & 1:
                total_w += weights[i]
                total_v += values[i]
                choice[i] = 1
        if total_w <= capacity and total_v > best_value:
            best_value = total_v
            best_choice = choice

    return best_value, best_choice


def compare_fractional_and_exact():
    """Сравнение результатов жадного алгоритма для дробного рюкзака
    с точным решением 0-1."""
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50

    frac_value, frac_taken = fractional_knapsack(values, weights, capacity)
    brute_value, brute_choice = brute_force_01(values, weights, capacity)

    print('Fractional (greedy) значение:', frac_value)
    print('0-1 значение:', brute_value)
    print('Fractional взятое:', frac_taken)
    print('0-1 выбор:', brute_choice)


def time_huffman_test(repetitions: int = 5):
    """Проведение замеров времени работы алгоритма Хаффмана."""
    import random
    from greedy_algorithms import huffman_codes

    sizes = [100, 1000, 5000, 10000]
    print('\nЗамеры Хаффмана:')
    for n in sizes:
        freqs = {str(i): random.randint(1, 1000) for i in range(n)}
        t0 = time.time()
        for _ in range(repetitions):
            _ = huffman_codes(freqs)
        t1 = time.time()
        avg = (t1 - t0) / repetitions
        print(f'n={n:6d} -> avg time {avg:.6f} sec')


if __name__ == '__main__':
    """Запуск анализа."""
    compare_fractional_and_exact()
    time_huffman_test()
