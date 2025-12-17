"""
Модуль для вычисления префикс-функции строки.
Префикс-функция π[i] — длина наибольшего собственного префикса,
который является суффиксом подстроки s[0..i].

Временная сложность: O(n)
Пространственная сложность: O(n)
"""


def prefix_function(s: str) -> list[int]:
    """
    Вычисляет префикс-функцию для строки.

    Параметры:
    s (str): Входная строка.

    Возвращает:
    list[int]: Массив π длины n.
    """
    n = len(s)
    pi = [0] * n

    for i in range(1, n):
        j = pi[i - 1]

        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1

        pi[i] = j

    return pi


def find_string_period(s: str) -> int:
    """
    Находит минимальный период строки с помощью префикс-функции.

    Параметры:
    s (str): Входная строка.

    Возвращает:
    int: Длина периода (0 если строка непериодическая).
    """
    n = len(s)
    if n <= 1:
        return 0

    pi = prefix_function(s)
    period = n - pi[-1]

    if n % period == 0 and period < n:
        if s[:period] * (n // period) == s:
            return period

    return 0


if __name__ == "__main__":
    test_string = "ababcabab"
    result = prefix_function(test_string)
    period = find_string_period(test_string)

    print(f"Строка: {test_string}")
    print(f"Префикс-функция: {result}")
    print(f"Период строки: {period}")
