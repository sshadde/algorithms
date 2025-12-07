"""Реализация универсальной кучи (min-heap и max-heap) на основе массива."""
from typing import List, Optional, Union


class Heap:
    """
    Универсальная куча (min-heap или max-heap).

    Attributes:
        heap (List): Массив для хранения элементов кучи.
        is_min (bool): True для min-heap, False для max-heap.
    """

    def __init__(self, is_min: bool = True):
        """
        Инициализация кучи.

        Args:
            is_min (bool): Тип кучи. По умолчанию min-heap.
        """
        self.heap: List[Union[int, float]] = []
        self.is_min = is_min

    def _compare(self, a: Union[int, float], b: Union[int, float]) -> bool:
        """
        Сравнение двух элементов в зависимости от типа кучи.

        Args:
            a: Первый элемент.
            b: Второй элемент.

        Returns:
            bool: True, если порядок нарушен и нужно менять местами.
        """
        if self.is_min:
            return a < b
        else:
            return a > b

    def _sift_up(self, index: int) -> None:
        """
        Всплытие элемента. Временная сложность: O(log n).

        Args:
            index: Индекс элемента, который нужно поднять.
        """
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self.heap[index], self.heap[parent]):
                self.heap[index], self.heap[parent] = (
                    self.heap[parent], self.heap[index]
                )
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        """
        Погружение элемента. Временная сложность: O(log n).

        Args:
            index: Индекс элемента, который нужно опустить.
        """
        size = len(self.heap)
        while 2 * index + 1 < size:
            left = 2 * index + 1
            right = 2 * index + 2
            child = left
            if right < size and self._compare(self.heap[right],
                                              self.heap[left]):
                child = right
            if self._compare(self.heap[child], self.heap[index]):
                self.heap[index], self.heap[child] = (
                    self.heap[child], self.heap[index]
                )
                index = child
            else:
                break

    def insert(self, value: Union[int, float]) -> None:
        """
        Вставка элемента в кучу. Временная сложность: O(log n).

        Args:
            value: Значение для вставки.
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def extract(self) -> Union[int, float]:
        """
        Извлечение корня кучи. Временная сложность: O(log n).

        Returns:
            Значение корня или None, если куча пуста.
        """
        if not self.heap:
            raise IndexError("Извлечение из пустой кучи!")
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return root

    def peek(self) -> Optional[Union[int, float]]:
        """
        Просмотр корня без извлечения. Временная сложность: O(1).

        Returns:
            Значение корня или None, если куча пуста.
        """
        return self.heap[0] if self.heap else None

    def build_heap(self, array: List[Union[int, float]]) -> None:
        """
        Построение кучи из произвольного массива. Временная сложность: O(n).

        Args:
            array: Исходный массив.
        """
        self.heap = array[:]
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __len__(self) -> int:
        """
        Возвращает количество элементов в куче.

        Returns:
            int: Размер кучи.
        """
        return len(self.heap)

    def __str__(self) -> str:
        """
        Строковое представление кучи.

        Returns:
            str: Строка с элементами кучи.
        """
        return str(self.heap)
