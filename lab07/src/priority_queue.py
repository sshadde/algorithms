"""Реализация приоритетной очереди на основе кучи."""
from typing import Any, Dict, List, Optional, Tuple, Union
from heap import Heap


class PriorityQueue:
    """
    Приоритетная очередь на основе кучи.

    Attributes:
        heap (Heap): Куча для хранения приоритетов.
        items (Dict): Словарь для хранения элементов по приоритетам.
    """

    def __init__(self, is_min: bool = True) -> None:
        """
        Инициализация приоритетной очереди.

        Args:
            is_min (bool): True для min-heap, False для max-heap.
        """
        self.heap = Heap(is_min=is_min)
        self.items: Dict[Union[int, float], List[Any]] = {}

    def enqueue(self, item: Any, priority: Union[int, float]) -> None:
        """
        Добавление элемента в очередь. Временная сложность: O(log n).

        Args:
            item (Any): Элемент для добавления.
            priority (Union[int, float]): Приоритет элемента.
        """
        self.heap.insert(priority)

        if priority not in self.items:
            self.items[priority] = []
        self.items[priority].append(item)

    def dequeue(self) -> Optional[Tuple[Union[int, float], Any]]:
        """
        Извлечение элемента с наивысшим приоритетом.

        Временная сложность: O(log n) + O(k), где k - количество элементов
        с одинаковым приоритетом.

        Returns:
            Optional[Tuple[Union[int, float], Any]]:
            Кортеж (приоритет, элемент)
            или None, если очередь пуста.
        """
        priority = self.heap.extract()
        if priority is None:
            return None

        if (priority in self.items and self.items[priority]):
            item = self.items[priority].pop(0)
            if not self.items[priority]:
                del self.items[priority]
            return (priority, item)

        return None

    def peek(self) -> Optional[Tuple[Union[int, float], Any]]:
        """
        Просмотр элемента с наивысшим приоритетом без извлечения.

        Временная сложность: O(1).

        Returns:
            Optional[Tuple[Union[int, float], Any]]:
            Кортеж (приоритет, элемент)
            или None, если очередь пуста.
        """
        priority = self.heap.peek()
        if priority is None or priority not in self.items:
            return None

        if self.items[priority]:
            return (priority, self.items[priority][0])

        return None

    def __len__(self) -> int:
        """
        Возвращает количество элементов в очереди.

        Returns:
            int: Количество элементов в очереди.
        """
        return len(self.heap)

    def is_empty(self) -> bool:
        """
        Проверка, пуста ли очередь.

        Returns:
            bool: True, если очередь пуста, иначе False.
        """
        return len(self.heap) == 0

    def __str__(self) -> str:
        """
        Строковое представление очереди.

        Returns:
            str: Строка с информацией о размере очереди.
        """
        return f"PriorityQueue(size={len(self)}, is_min={self.heap.is_min})"
