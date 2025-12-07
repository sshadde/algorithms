"""Реализация сортировки кучей (Heapsort) in-place."""
from typing import List, Union
from heap import Heap


def heapsort(array: List[Union[int, float]], ascending: bool = True) -> None:
    """
    Сортировка кучей (in-place). Временная сложность: O(n log n).

    Args:
        array: Массив для сортировки.
        ascending: True для сортировки по возрастанию, False для убывания.
    """
    is_min = not ascending
    heap = Heap(is_min=is_min)
    heap.build_heap(array)

    for i in range(len(array) - 1, -1, -1):
        array[i] = heap.extract()
