"""Модуль для сравнительного анализа разных подходов"""
import time
from dynamic_programming import Fibonacci, Knapsack01


def measure_time(func, *args, repetitions=1000):
    """Измеряет среднее время выполнения функции"""

    for _ in range(10):
        func(*args)

    start = time.perf_counter()
    for _ in range(repetitions):
        result = func(*args)
    end = time.perf_counter()

    return result, (end - start) / repetitions


def compare_fibonacci_approaches():
    """Сравнение разных подходов для чисел Фибоначчи"""

    print("=== Сравнение подходов для чисел Фибоначчи ===")

    test_values = [5, 10, 20, 30, 40]

    for n in test_values:
        print(f"\nДля n = {n}:")

        if n <= 30:
            start = time.perf_counter()
            result = Fibonacci.naive_recursive(n)
            naive_time = time.perf_counter() - start
            print(
                f"  Наивная рекурсия: {result} (время: {naive_time:.6f} сек)")

        start = time.perf_counter()
        result = Fibonacci.memoization(n)
        memo_time = time.perf_counter() - start
        print(f"  Мемоизация: {result} (время: {memo_time:.6f} сек)")

        start = time.perf_counter()
        result = Fibonacci.bottom_up(n)
        bottom_up_time = time.perf_counter() - start
        print(
            f"  Восходящий подход: {result} (время: {bottom_up_time:.6f} сек)")


def compare_knapsack_approaches():
    """Сравнение жадного алгоритма и ДП для рюкзака"""

    print("\n=== Сравнение подходов для задачи о рюкзаке ===")

    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    print(f"Предметы (вес/стоимость): {list(zip(weights, values))}")
    print(f"Вместимость рюкзака: {capacity}")

    print("\n1. Жадный алгоритм (непрерывный рюкзак):")

    greedy_result = Knapsack01.greedy_fractional(weights, values, capacity)
    print(f"   Фактический результат: {greedy_result:.2f}")

    print("\n2. Динамическое программирование (0-1 рюкзак):")

    dp_result, selected = Knapsack01.bottom_up(weights, values, capacity)
    print(f"   Фактический результат: {dp_result}")
    print(f"   Выбранные предметы (индексы): {selected}")

    print("\n" + "="*60)

    print("\nВывод:")
    print("Жадный алгоритм дал результат 240.00, но это для")
    print("непрерывного рюкзака (можно брать части предметов).")
    print("Для 0-1 рюкзака ДП дал результат 220, что является")
    print("оптимальным решением для задачи без дробления предметов.")


def performance_analysis():
    """Анализ производительности при увеличении размера задачи"""

    print("\n=== Анализ масштабируемости алгоритмов ДП ===")

    print("Тестируем задачу о рюкзаке:")

    import random

    for n in [5, 10, 20, 30]:
        weights = [random.randint(1, 20) for _ in range(n)]
        values = [random.randint(1, 50) for _ in range(n)]
        capacity = sum(weights) // 2

        start = time.perf_counter()
        result, _ = Knapsack01.bottom_up(weights, values, capacity)
        elapsed = time.perf_counter() - start

        print(f"  n={n}: время={elapsed:.6f} сек, результат={result}")


if __name__ == "__main__":
    fib_results = compare_fibonacci_approaches()
    compare_knapsack_approaches()
    performance_analysis()
