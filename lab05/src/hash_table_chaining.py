"""Метод цепочек с динамическим масштабированием."""
from typing import Any, Callable, List, Tuple
from hash_functions import djb2_hash


class HashTableChaining:
    def __init__(self, size: int = 10, hash_func: Callable = djb2_hash):
        """
        Хеш-таблица методом цепочек.

        Args:
            size: Размер хеш-таблицы
            hash_func: Хеш-функция. По умолчанию используется djb2_hash
        """
        self.size = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]
        self.hash_func = hash_func

    def insert(self, key: str, value: Any):
        """
        Вставка элемента.

        Сложность:
        - Средний случай: O(1 + α)
        - Худший случай: O(n)
        """
        index = self.hash_func(key, self.size)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def search(self, key: str) -> Any:
        """
        Поиск элемента.

        Сложность:
        - Средний случай: O(1 + α)
        - Худший случай: O(n)
        """
        index = self.hash_func(key, self.size)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key: str):
        """
        Удаление элемента.

        Сложность:
        - Средний случай: O(1 + α)
        - Худший случай: O(n)
        """
        index = self.hash_func(key, self.size)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return
