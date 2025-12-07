"""Модуль с реализациями алгоритмов динамического программирования"""
from functools import lru_cache


class Fibonacci:
    """Класс для демонстрации различных способов вычисления чисел Фибоначчи"""

    @staticmethod
    def naive_recursive(n: int) -> int:
        """
        Наивная рекурсивная реализация (медленная)
        Сложность: O(2^n) - экспоненциальная
        """
        if n <= 1:
            return n
        return Fibonacci.naive_recursive(n-1) + Fibonacci.naive_recursive(n-2)

    @staticmethod
    @lru_cache(maxsize=None)
    def memoization(n: int) -> int:
        """
        Рекурсия с мемоизацией (кэшированием результатов)
        Сложность: O(n) - линейная
        Пространственная сложность: O(n)
        """
        if n <= 1:
            return n
        return Fibonacci.memoization(n-1) + Fibonacci.memoization(n-2)

    @staticmethod
    def bottom_up(n: int) -> int:
        """
        Восходящий подход (табличный)
        Сложность: O(n) - линейная
        Пространственная сложность: O(1) - хранение лишь двух чисел
        """
        if n <= 1:
            return n

        prev, current = 0, 1
        for _ in range(2, n + 1):
            prev, current = current, prev + current
        return current


class Knapsack01:
    """Решение задачи о рюкзаке 0-1 методом динамического программирования"""

    @staticmethod
    def bottom_up(weights: list, values: list, capacity: int) -> tuple:
        """
        Восходящий подход для задачи о рюкзаке
        Сложность: O(n * W), где n - количество предметов, W - вместимость
        Пространственная сложность: O(n * W)

        Возвращает: (максимальная стоимость, выбранные предметы)
        """
        n = len(weights)

        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        dp[i-1][w],
                        dp[i-1][w - weights[i-1]] + values[i-1]
                    )
                else:
                    dp[i][w] = dp[i-1][w]

        selected_items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(i-1)
                w -= weights[i-1]

        selected_items.reverse()
        return dp[n][capacity], selected_items

    @staticmethod
    def greedy_fractional(weights: list, values: list, capacity: int) -> float:
        """
        Жадный алгоритм для непрерывного рюкзака

        Можно брать части предметов
        """
        items = []
        for i in range(len(weights)):
            if weights[i] > 0:
                ratio = values[i] / weights[i]
                items.append((ratio, weights[i], values[i], i))

        items.sort(reverse=True)

        total_value = 0.0
        remaining_capacity = capacity

        for ratio, weight, value, idx in items:
            if remaining_capacity >= weight:
                total_value += value
                remaining_capacity -= weight
            else:
                fraction = remaining_capacity / weight
                total_value += value * fraction
                break

        return total_value


class LCS:
    """Нахождение наибольшей общей подпоследовательности"""

    @staticmethod
    def bottom_up(str1: str, str2: str) -> tuple:
        """
        Восходящий подход для LCS
        Сложность: O(m * n), где m, n - длины строк
        Пространственная сложность: O(m * n)

        Возвращает: (длина LCS, сама подпоследовательность)
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if str1[i-1] == str2[j-1]:
                lcs_chars.append(str1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        lcs_chars.reverse()
        lcs_string = ''.join(lcs_chars)

        return dp[m][n], lcs_string


class Levenshtein:
    """Вычисление редакционного расстояния между строками"""

    @staticmethod
    def bottom_up(str1: str, str2: str) -> int:
        """
        Восходящий подход для расстояния Левенштейна
        Сложность: O(m * n)
        Пространственная сложность: O(m * n)
        """
        m, n = len(str1), len(str2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    cost = 0
                else:
                    cost = 1

                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + cost
                )

        return dp[m][n]


class CoinChange:
    """Минимальное количество монет для суммы"""

    @staticmethod
    def min_coins(coins: list, amount: int) -> int:
        """
        Находит минимальное количество монет для суммы
        Сложность: O(n * amount)
        """
        dp = [10**10] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != 10**10 else -1


class LIS:
    """Наибольшая возрастающая подпоследовательность"""

    @staticmethod
    def length(nums: list) -> int:
        """
        Находит длину наибольшей возрастающей подпоследовательности
        Сложность: O(n^2)
        """
        if not nums:
            return 0

        n = len(nums)
        dp = [1] * n

        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)
