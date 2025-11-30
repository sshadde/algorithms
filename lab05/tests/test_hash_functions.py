import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hash_functions import (  # type: ignore # noqa: E402
    simple_hash, polynomial_hash, djb2_hash
    )


def test_hash_functions_basic():
    """Базовое тестирование хеш-функций."""
    print("Тестирование хеш-функций...")

    test_strings = ["apple", "banana", "hello", "world", "test"]
    table_size = 100

    for hash_func in [simple_hash, polynomial_hash, djb2_hash]:
        print(f"  Функция: {hash_func.__name__}")

        hash1 = hash_func("apple", table_size)
        hash2 = hash_func("apple", table_size)
        assert hash1 == hash2, "Хеш-функция должна быть детерминированной"
        print("    ✓ Детерминированность")

        for s in test_strings:
            h = hash_func(s, table_size)
            assert 0 <= h < table_size, f"Хеш {h} вне "
            f"диапазона [0, {table_size-1}]"
        print("    ✓ В пределах диапазона")

        hashes = [hash_func(s, table_size) for s in test_strings]
        unique_hashes = len(set(hashes))
        assert unique_hashes >= 2, "Слишком много коллизий для разных строк"
        print(f"    ✓ Распределение ({unique_hashes}/5 уникальных хешей)")


def test_hash_collisions():
    """Тестирование на коллизии."""
    print("Тестирование коллизий...")

    table_size = 10

    test_pairs = [
        ("ab", "ba"),
        ("abc", "acb"),
        ("test", "tset")
    ]

    for hash_func in [simple_hash, polynomial_hash, djb2_hash]:
        collisions = 0
        for s1, s2 in test_pairs:
            if hash_func(s1, table_size) == hash_func(s2, table_size):
                collisions += 1

        print(f"  {hash_func.__name__}: {collisions}/{len(test_pairs)} "
              f"коллизий")
        if hash_func.__name__ == "simple_hash":
            assert collisions >= 1, "simple_hash должен "
            "иметь коллизии для анаграмм"
        else:
            print(f"    (допустимо для {hash_func.__name__})")


def test_hash_distribution():
    """Тестирование равномерности распределения."""
    print("Тестирование распределения...")

    table_size = 20
    test_strings = [f"key{i}" for i in range(50)]

    for hash_func in [simple_hash, polynomial_hash, djb2_hash]:
        hashes = [hash_func(s, table_size) for s in test_strings]

        distribution = [0] * table_size
        for h in hashes:
            distribution[h] += 1

        empty_cells = distribution.count(0)
        max_cells = max(distribution)

        print(
            f"  {hash_func.__name__}: {empty_cells} пустых ячеек, "
            f"максимум {max_cells} в ячейке")


if __name__ == "__main__":
    test_hash_functions_basic()
    print()
    test_hash_collisions()
    print()
    test_hash_distribution()
    print("\nВсе тесты хеш-функций пройдены!")
