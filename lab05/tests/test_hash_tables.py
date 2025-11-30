# flake8: noq: E402
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


from hash_table_open_addressing import (  # type: ignore # noqa: E402
    HashTableOpenAddressing
    )
from hash_table_chaining import (  # type: ignore # noqa: E402
    HashTableChaining
    )


def test_chaining():
    """Тестирование метода цепочек."""
    print("Тестирование метода цепочек...")

    table = HashTableChaining(size=5)

    table.insert("apple", 10)
    table.insert("banana", 20)
    assert table.search("apple") == 10
    assert table.search("banana") == 20
    print("✓ Базовая вставка и поиск")

    table.insert("apple", 100)
    assert table.search("apple") == 100
    print("✓ Обновление значения")

    table.delete("banana")
    assert table.search("banana") is None
    print("✓ Удаление элемента")

    assert table.search("grape") is None
    print("✓ Поиск несуществующего элемента")


def test_chaining_collisions():
    """Тестирование обработки коллизий в методе цепочек."""
    print("Тестирование коллизий...")

    def collision_hash(key: str, table_size: int) -> int:
        return 0

    table = HashTableChaining(size=5, hash_func=collision_hash)

    table.insert("key1", "value1")
    table.insert("key2", "value2")
    table.insert("key3", "value3")

    assert table.search("key1") == "value1"
    assert table.search("key2") == "value2"
    assert table.search("key3") == "value3"
    print("✓ Все элементы найдены несмотря на коллизии")

    table.delete("key2")
    assert table.search("key1") == "value1"
    assert table.search("key2") is None
    assert table.search("key3") == "value3"
    print("✓ Удаление из середины цепочки")


def test_open_addressing():
    """Тестирование открытой адресации."""
    print("Тестирование открытой адресации...")

    for probe_method in ["linear", "double"]:
        print(f"Метод пробирования: {probe_method}")
        table = HashTableOpenAddressing(size=5, probe_method=probe_method)

        table.insert("apple", 10)
        table.insert("banana", 20)
        assert table.search("apple") == 10
        assert table.search("banana") == 20
        print("  ✓ Базовая вставка и поиск")

        table.insert("apple", 100)
        assert table.search("apple") == 100
        print("  ✓ Обновление значения")

        table.delete("banana")
        assert table.search("banana") is None
        print("  ✓ Удаление элемента")

        assert table.search("grape") is None
        print("  ✓ Поиск несуществующего элемента\n")


def test_both_methods_comparison():
    """Сравниваем работу обоих методов на одинаковых данных."""
    print("Сравнение методов...")

    test_data = [
        ("apple", 1),
        ("banana", 2),
        ("orange", 3),
        ("grape", 4),
        ("kiwi", 5)
    ]

    chaining_table = HashTableChaining(size=10)
    open_table = HashTableOpenAddressing(size=10, probe_method="linear")

    for key, value in test_data:
        chaining_table.insert(key, value)
        open_table.insert(key, value)

    for key, expected_value in test_data:
        assert chaining_table.search(key) == expected_value
        assert open_table.search(key) == expected_value

    print("✓ Оба метода работают согласованно")


if __name__ == "__main__":
    test_chaining()
    print()
    test_chaining_collisions()
    print()
    test_open_addressing()
    test_both_methods_comparison()
    print("\nВсе тесты пройдены!")
