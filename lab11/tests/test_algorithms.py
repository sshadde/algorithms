"""Модульные тесты для алгоритмов на строках."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from string_matching import rabin_karp_search  # type: ignore  # noqa: E402
from kmp_search import kmp_search  # type: ignore  # noqa: E402
from z_function import (  # type: ignore  # noqa: E402
    z_function, z_search, is_cyclic_shift
)
from prefix_function import (  # type: ignore  # noqa: E402
    prefix_function, find_string_period
)


def test_prefix_function() -> None:
    """Тест префикс-функции."""
    assert prefix_function("ababcabab") == [0, 0, 1, 2, 0, 1, 2, 3, 4]
    assert prefix_function("aaaaa") == [0, 1, 2, 3, 4]
    assert prefix_function("") == []
    print("✓ Prefix function works correctly")


def test_find_string_period() -> None:
    """Тест поиска периода строки."""
    assert find_string_period("abcabcabc") == 3
    assert find_string_period("aaaaa") == 1
    assert find_string_period("ababab") == 2
    assert find_string_period("abcdef") == 0
    assert find_string_period("a") == 0
    assert find_string_period("") == 0
    print("✓ String period detection works correctly")


def test_kmp_search() -> None:
    """Тест алгоритма KMP."""
    assert kmp_search("ababcababcab", "ababc") == [0, 5]
    assert kmp_search("aaaaa", "aa") == [0, 1, 2, 3]
    assert kmp_search("abcdef", "xyz") == []
    print("✓ KMP algorithm works correctly")


def test_z_function() -> None:
    """Тест Z-функции."""
    assert z_function("abacaba") == [0, 0, 1, 0, 3, 0, 1]
    assert z_function("aaaaa") == [0, 4, 3, 2, 1]
    assert z_function("") == []
    print("✓ Z-function works correctly")


def test_z_search() -> None:
    """Тест поиска через Z-функцию."""
    assert z_search("ababcababcab", "ababc") == [0, 5]
    assert z_search("aaaaa", "aa") == [0, 1, 2, 3]
    print("✓ Z-search works correctly")


def test_is_cyclic_shift() -> None:
    """Тест проверки циклического сдвига."""
    assert is_cyclic_shift("abcdef", "defabc") is True
    assert is_cyclic_shift("abcdef", "fedcba") is False
    assert is_cyclic_shift("abc", "abcd") is False
    print("✓ Cyclic shift detection works correctly")


def test_rabin_karp_search() -> None:
    """Тест алгоритма Рабина-Карпа."""
    assert rabin_karp_search("ababcababcab", "ababc") == [0, 5]
    assert rabin_karp_search("aaaaa", "aa") == [0, 1, 2, 3]
    assert rabin_karp_search("abcdef", "xyz") == []
    print("✓ Rabin-Karp algorithm works correctly")


def run_all_tests() -> None:
    """Запуск всех тестов."""
    test_prefix_function()
    test_find_string_period()
    test_kmp_search()
    test_z_function()
    test_z_search()
    test_is_cyclic_shift()
    test_rabin_karp_search()

    print("\nAll tests passed!")


if __name__ == "__main__":
    run_all_tests()
