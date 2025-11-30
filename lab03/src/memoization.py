"""Модуль с реализацией мемоизации для оптимизации рекурсивных алгоритмов."""

import time
import matplotlib.pyplot as plt
from typing import Dict, Optional

from recursion import fibonacci


def fibonacci_memo(n: int, counter: Optional[list] = None,
                   memo: Optional[Dict[int, int]] = None,) -> int:
    """
    Вычисление n-го числа Фибоначчи с мемоизацией.

    Args:
        n: Порядковый номер числа Фибоначчи
        counter: Счетчик вызовов
        memo: Словарь для кеширования результатов
    Returns:
        n-е число Фибоначчи
    """
    if counter is None:
        counter = [0]

    counter[0] += 1

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = (fibonacci_memo(n - 1, counter, memo) +
               fibonacci_memo(n - 2, counter, memo))
    return memo[n]
# Временная сложность: O(n)
# Глубина рекурсии: O(n)


def compare_fibonacci_performance() -> None:
    """Сравнение производительности наивной и мемоизированной версий."""
    print('=== Сравнение производительности ===')

    n_values = [5, 10, 15, 20, 25, 30, 35]
    naive_times = []
    memo_times = []
    naive_calls_list = []
    memo_calls_list = []

    for n in n_values:
        print(f"n={n}:", end=" ")

        counter = [0]
        start_time = time.time()
        naive_result = fibonacci(n, counter)
        naive_time = time.time() - start_time
        naive_calls = counter[0]

        counter = [0]
        start_time = time.time()
        memo_result = fibonacci_memo(n, counter)
        memo_time = time.time() - start_time
        memo_calls = counter[0]

        # Проверяем корректность
        assert naive_result == memo_result, "Результаты не совпадают!"

        naive_times.append(naive_time)
        memo_times.append(memo_time)
        naive_calls_list.append(naive_calls)
        memo_calls_list.append(memo_calls)

        print(f"наивная={naive_time:.6f}с ({naive_calls:,} вызовов), "
              f"мемоизация={memo_time:.6f}с ({memo_calls} вызовов)")

    # Строим графики
    plot_results(n_values, naive_times, memo_times,
                 naive_calls_list, memo_calls_list)


def plot_results(n_values, naive_times, memo_times, naive_calls, memo_calls):
    """Построение графиков времени выполнения."""
    # График времени выполнения
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(n_values, naive_times, 'ro-',
             label='Наивная рекурсия', linewidth=2)
    plt.plot(n_values, memo_times, 'go-',
             label='С мемоизацией', linewidth=2)
    plt.xlabel('n')
    plt.ylabel('Время (секунды)')
    plt.title('Время выполнения')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('lab03/report/fibonacci_time_comparison.png',
                dpi=300, bbox_inches='tight')

    # График количества вызовов
    plt.figure(figsize=(8, 5))
    plt.semilogy(n_values, naive_calls, 'bo-',
                 label='Наивная рекурсия', linewidth=2)
    plt.plot(n_values, memo_calls, 'mo-',
             label='С мемоизацией', linewidth=2)
    plt.xlabel('n')
    plt.ylabel('Количество вызовов')
    plt.title('Количество рекурсивных вызовов')
    plt.legend()
    plt.grid(True)
    plt.savefig('lab03/report/fibonacci_calls_comparison.png',
                dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    compare_fibonacci_performance()
