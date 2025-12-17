"""
Модуль для вычисления Z-функции строки.
Z[i] - длина наибольшего общего префикса строки s и суффикса s[i..].

Временная сложность: O(n)
Пространственная сложность: O(n)
"""


def z_function(s: str) -> list[int]:
    """
    Вычисляет Z-функцию для строки.

    Параметры:
    s (str): Входная строка.

    Возвращает:
    list[int]: Массив Z длины n.
    """
    n = len(s)
    z = [0] * n
    left = right = 0

    for i in range(1, n):
        if i <= right:
            z[i] = min(right - i + 1, z[i - left])

        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > right:
            left, right = i, i + z[i] - 1

    return z


def is_cyclic_shift(s1: str, s2: str) -> bool:
    """
    Проверяет, является ли строка s2 циклическим сдвигом строки s1.

    Параметры:
    s1 (str): Первая строка.
    s2 (str): Вторая строка.

    Возвращает:
    bool: True если s2 - циклический сдвиг s1.
    """
    if len(s1) != len(s2):
        return False

    combined = s1 + "#" + s2 + s2
    z = z_function(combined)

    len1 = len(s1)
    for i in range(len1 + 1, len(z)):
        if z[i] == len1:
            return True
    return False


def z_search(text: str, pattern: str) -> list[int]:
    """
    Поиск подстроки в тексте с использованием Z-функции.

    Параметры:
    text (str): Исходный текст.
    pattern (str): Искомый шаблон.

    Возвращает:
    list[int]: Список индексов начала вхождений.
    """
    if not pattern:
        return []

    combined = pattern + "#" + text
    z = z_function(combined)
    result = []
    pattern_len = len(pattern)

    for i in range(pattern_len + 1, len(z)):
        if z[i] == pattern_len:
            result.append(i - pattern_len - 1)

    return result


if __name__ == "__main__":
    test_string = "abacaba"
    result = z_function(test_string)

    s1 = "abcdef"
    s2 = "defabc"
    is_shift = is_cyclic_shift(s1, s2)

    print(f"Строка: {test_string}")
    print(f"Z-функция: {result}")
    print(f"'{s2}' является циклическим сдвигом '{s1}': {is_shift}")
