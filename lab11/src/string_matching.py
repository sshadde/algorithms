"""
Модуль для дополнительных алгоритмов поиска подстрок.
Реализован алгоритм Рабина-Карпа с полиномиальным хэшированием.

Временная сложность: в среднем O(n+m), в худшем O(n*m)
Пространственная сложность: O(1)
"""


def rabin_karp_search(text: str, pattern: str, base: int = 256,
                      mod: int = 10**9 + 7) -> list[int]:
    """
    Ищет все вхождения подстроки в строку с помощью алгоритма Рабина-Карпа.

    Параметры:
    text (str): Исходный текст.
    pattern (str): Искомый шаблон.
    base (int): Основание системы счисления для хэша.
    mod (int): Модуль для предотвращения переполнения.

    Возвращает:
    list[int]: Список индексов начала вхождений.
    """
    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return []

    pattern_hash = 0
    window_hash = 0
    h = pow(base, pattern_len - 1, mod)

    for i in range(pattern_len):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    result = []

    for i in range(text_len - pattern_len + 1):
        if pattern_hash == window_hash:
            if text[i:i + pattern_len] == pattern:
                result.append(i)

        if i < text_len - pattern_len:
            window_hash = (base * (window_hash - ord(text[i]) * h) +
                           ord(text[i + pattern_len])) % mod
            window_hash = (window_hash + mod) % mod

    return result


if __name__ == "__main__":
    text = "ababcababcab"
    pattern = "ababc"
    indices = rabin_karp_search(text, pattern)

    print(f"Текст: {text}")
    print(f"Шаблон: {pattern}")
    print(f"Индексы вхождений (Рабин-Карп): {indices}")
