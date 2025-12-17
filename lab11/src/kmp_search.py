"""
Модуль для поиска подстроки в строке с помощью алгоритма Кнута-Морриса-Пратта.
Использует префикс-функцию для избежания лишних сравнений.

Временная сложность: O(n + m)
Пространственная сложность: O(m)
"""

from prefix_function import prefix_function


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Ищет все вхождения подстроки pattern в строку text.

    Параметры:
    text (str): Исходный текст.
    pattern (str): Искомый шаблон.

    Возвращает:
    list[int]: Список индексов начала вхождений.
    """
    if not pattern:
        return []

    pi = prefix_function(pattern)
    result = []
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            result.append(i - j + 1)
            j = pi[j - 1]

    return result


if __name__ == "__main__":
    text = "ababcababcab"
    pattern = "ababc"
    indices = kmp_search(text, pattern)
    print(f"Текст: {text}")
    print(f"Шаблон: {pattern}")
    print(f"Индексы вхождений: {indices}")
