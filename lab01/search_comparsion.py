"""Сравнение алгоритмов поиска - линейного и бинарного."""
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
import time


def linear_search(arr: List[int], target: int) -> Optional[int]:
    """Функция линейного поиска."""
    # O(1) - инициализация переменных.
    i = 0  # O(1).
    # O(n) - в худшем случае придётся проверить все элементы.
    while i < len(arr):  # O(n).
        # O(1) - доступ к элементу по индексу.
        if arr[i] == target:  # O(1).
            # O(1) - возврат индекса.
            return i  # O(1).
        # O(1) - инкремент.
        i += 1  # O(1).
    # O(1) - если элемент не найден.
    return None  # O(1).
# Общая сложность: O(n).


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """Функция бинарного поиска."""
    # O(1) - инициализация границ.
    left = 0  # O(1).
    right = len(arr) - 1  # O(1).
    # O(log n) - количество итераций фукнции в худшем случае.
    while left <= right:  # O(log n).
        # O(1) - вычисление среднего.
        mid = (left + right) // 2  # O(1).
        # O(1) - доступ к элементу.
        if arr[mid] == target:  # O(1).
            return mid  # O(1).
        # O(1) - сравнение и сдвиг границ.
        if arr[mid] < target:  # O(1).
            left = mid + 1  # O(1).
        else:
            right = mid - 1  # O(1).
    return None  # O(1)
# Общая сложность: O(log n).


def generate_sorted_array(n: int) -> List[int]:
    """Функция генерации отсортированного массива."""
    # O(n) - создание листа длины n.
    return list(range(n))  # O(n).


def time_function(func, arr: List[int],
                  target: int,
                  repeats: int = 5) -> float:
    """Функция замера времени."""
    # O(repeats) - выполняем несколько повторов и усредняем.
    total = 0.0  # O(1).
    for _ in range(repeats):  # O(repeats).
        start = time.perf_counter()  # O(1).
        _ = func(arr, target)  # O(cost of func).
        end = time.perf_counter()  # O(1).
        total += (end - start)  # O(1).
    return total / repeats  # O(1).


def run_experiments(sizes: List[int]) -> Dict[str, Dict[int, float]]:
    """
    Функция запуска замеров.

    Для каждого размера:
      - создаём отсортированный массив,
      - выбираем цели: первый (0), средний, последний, отсутствующий (-1)
      - замеряем среднее время для linear_search и binary_search.
    """
    results: Dict[str, Dict[int, float]] = {'linear': {}, 'binary': {}}  # O(1)
    for n in sizes:  # O(len(sizes)).
        arr = generate_sorted_array(n)  # O(n).
        targets = {
            'first': arr[0],  # O(1).
            'middle': arr[n // 2],  # O(1).
            'last': arr[-1],  # O(1).
            'missing': -1  # O(1) (элемент которого нет в массиве).
        }
        # Сосчитаем среднее время для поиска (на примере target = middle).
        t_lin = time_function(linear_search, arr, targets['middle'])  # O(time)
        t_bin = time_function(binary_search, arr, targets['middle'])  # O(time)
        results['linear'][n] = t_lin  # O(1).
        results['binary'][n] = t_bin  # O(1).
    return results  # O(1).


def plot_results(results: Dict[str, Dict[int, float]]) -> None:
    """Функция визуализации результатов."""
    sizes = sorted(results['linear'].keys())
    linear_times = [results['linear'][n] for n in sizes]
    binary_times = [results['binary'][n] for n in sizes]

    # Линейный масштаб.
    plt.figure()
    plt.plot(sizes, linear_times, label='Linear Search')  # O(n) для построения
    plt.plot(sizes, binary_times, label='Binary Search')
    plt.xlabel('Size of array (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Search time vs n (linear scale)')
    plt.legend()
    plt.grid(True)
    plt.savefig('results_linear.png')  # Сохраняем картинку.
    plt.close()

    # Логарифмический масштаб по y.
    plt.figure()
    plt.plot(sizes, linear_times, label='Linear Search')
    plt.plot(sizes, binary_times, label='Binary Search')
    plt.yscale('log')  # Логарифмическая шкала по Y.
    plt.xlabel('Size of array (n)')
    plt.ylabel('Time (seconds, log scale)')
    plt.title('Search time vs n (log scale)')
    plt.legend()
    plt.grid(True)
    plt.savefig('results_log.png')
    plt.close()
