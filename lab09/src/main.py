"""Основной файл для демонстрации работы всех алгоритмов"""

from dynamic_programming import (
    Fibonacci, Knapsack01, LCS, Levenshtein,
    CoinChange, LIS
)
from comparison import (
    compare_fibonacci_approaches,
    compare_knapsack_approaches,
    performance_analysis
)


def demo_all_algorithms():
    """Демонстрация работы всех реализованных алгоритмов"""

    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ДИНАМИЧЕСКОГО ПРОГРАММИРОВАНИЯ")
    print("=" * 60)

    print("\n1. ЧИСЛА ФИБОНАЧЧИ")
    n = 10
    print(f"F({n}) =")
    print(f"  Наивная рекурсия: {Fibonacci.naive_recursive(n)}")
    print(f"  С мемоизацией: {Fibonacci.memoization(n)}")
    print(f"  Восходящий подход: {Fibonacci.bottom_up(n)}")

    print("\n2. ЗАДАЧА О РЮКЗАКЕ 0-1")
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    max_value, items = Knapsack01.bottom_up(weights, values, capacity)
    print(f"Веса: {weights}, Стоимости: {values}, Вместимость: {capacity}")
    print(f"Максимальная стоимость: {max_value}")
    print(f"Выбранные предметы (индексы): {items}")

    print("\n3. НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ")
    str1 = "ABCBDAB"
    str2 = "BDCABA"
    length, subsequence = LCS.bottom_up(str1, str2)
    print(f"Строка 1: {str1}")
    print(f"Строка 2: {str2}")
    print(f"Длина LCS: {length}")
    print(f"LCS: {subsequence}")

    print("\n4. РАССТОЯНИЕ ЛЕВЕНШТЕЙНА")
    str1 = "kitten"
    str2 = "sitting"
    distance = Levenshtein.bottom_up(str1, str2)
    print(f"'{str1}' -> '{str2}': {distance} операций")

    print("\n5. РАЗМЕН МОНЕТ")
    coins = [1, 2, 5]
    amount = 11
    min_coins = CoinChange.min_coins(coins, amount)
    print(f"Монеты: {coins}, Сумма: {amount}")
    print(f"Минимальное количество монет: {min_coins}")

    print("\n6. НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    lis_length = LIS.length(nums)
    print(f"Последовательность: {nums}")
    print(f"Длина LIS: {lis_length}")

    print("\n" + "=" * 60)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ")
    print("=" * 60)

    compare_fibonacci_approaches()
    compare_knapsack_approaches()
    performance_analysis()


if __name__ == "__main__":
    demo_all_algorithms()
