"""Метод открытой адресации."""
from typing import Any, Callable, Optional, List, Tuple
from hash_functions import djb2_hash


class HashTableOpenAddressing:
    def __init__(self, size: int = 10, probe_method: str = "linear",
                 hash_func: Callable = djb2_hash):
        """
        Хеш-таблица с открытой адресацией.

        Args:
            size: Размер хеш-таблицы
            probe_method: Метод пробирования ("linear" или "double")
            hash_func: Хеш-функция. По умолчанию используется djb2_hash
        """
        self.size = size
        self.table: List[Optional[Tuple[str, Any]]] = [None] * size
        self.probe_method = probe_method
        self.hash_func = hash_func
        self.count = 0

    def _probe_sequence(self, key: str, i: int) -> int:
        """
        Генерирует последовательность проб в зависимости от метода.

        Сложность: O(1)
        """
        if self.probe_method == "linear":
            return (self.hash_func(key, self.size) + i) % self.size
        elif self.probe_method == "double":
            h1 = self.hash_func(key, self.size)
            h2 = 1 + (self.hash_func(key, self.size - 1) % (self.size - 1))
            return (h1 + i * h2) % self.size
        else:
            raise ValueError("Неизвестный метод пробирования")

    def insert(self, key: str, value: Any) -> None:
        """
        Вставка элемента в хеш-таблицу.

        Сложность:
        - Средний случай: O(1/(1 - α))
        - Худший случай: O(n)
        """
        if self.count >= self.size * 0.9:
            raise Exception("Хеш-таблица почти заполнена")

        for i in range(self.size):
            index = self._probe_sequence(key, i)
            item = self.table[index]

            if item is None or item[0] == "__DELETED__":
                self.table[index] = (key, value)
                self.count += 1
                return

            if item[0] == key:
                self.table[index] = (key, value)
                return

        raise Exception("Не удалось найти место для вставки")

    def search(self, key: str) -> Optional[Any]:
        """
        Поиск элемента в хеш-таблице.

        Сложность:
        - Средний случай: O(1/(1 - α))
        - Худший случай: O(n)
        """
        for i in range(self.size):
            index = self._probe_sequence(key, i)
            item = self.table[index]

            if item is None:
                return None

            if item[0] == key:
                return item[1]

        return None

    def delete(self, key: str) -> None:
        """
        Удаление элемента из хеш-таблицы.

        Сложность:
        - Средний случай: O(1/(1 - α))
        - Худший случай: O(n)
        """
        for i in range(self.size):
            index = self._probe_sequence(key, i)
            item = self.table[index]

            if item is None:
                return

            if item[0] == key:
                self.table[index] = ("__DELETED__", None)
                self.count -= 1
                return
