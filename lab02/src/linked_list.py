from __future__ import annotations
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """Узел связного списка.
    Атрибуты:
        value: Значение, хранимое в узле.
        next: Ссылка на следующий узел или None.
    """
    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: Optional[Node[T]] = None


class LinkedList(Generic[T]):
    """Односвязный список с поддержкой head и tail.
    Реализованы методы вставки в начало и конец, удаления из начала,
    проход по списку и получение длины. Асимптотика:
      - insert_at_start: O(1)
      - insert_at_end: O(1)
      - delete_from_start: O(1)
      - traversal: O(n)
      - __len__: O(1)
    """
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.size: int = 0

    def insert_at_start(self, value: T) -> None:
        """Вставка значения в начало списка (O(1))."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert_at_end(self, value: T) -> None:
        """Вставка значения в конец списка (O(1) благодаря tail)."""
        new_node = Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def delete_from_start(self) -> Optional[T]:
        """Удаление первого элемента списка и возвращение его значения.
        Возвращает None, если список пуст.
        Оценка сложности: O(1).
        """
        if self.head is None:
            return None
        val = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return val

    def traversal(self) -> List[T]:
        """Проход по списку и сбор значений в список (O(n))."""
        res: List[T] = []
        node = self.head
        while node is not None:
            res.append(node.value)
            node = node.next
        return res

    def __len__(self) -> int:
        """Количество элементов в списке (O(1))."""
        return self.size


if __name__ == '__main__':
    ll = LinkedList[int]()
    ll.insert_at_end(1)
    ll.insert_at_start(0)
    ll.insert_at_end(2)
    print('Traversal:', ll.traversal())
    print('Deleted:', ll.delete_from_start())
    print('Len:', len(ll))
