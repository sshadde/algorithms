from __future__ import annotations
from collections import deque
from typing import Callable, List
import timeit
from linked_list import LinkedList


def time_func(func: Callable[[], None], number: int = 5) -> float:
    """Вернуть среднее время одного запуска функции в миллисекундах."""
    total = timeit.timeit(func, number=number)
    return (total / number) * 1000.0


def benchmark_insert_start_list(n: int, runs: int = 5) -> float:
    """Вставка n элементов в начало list (каждая insert O(n))."""
    def run() -> None:
        lst: List[int] = []
        for i in range(n):
            lst.insert(0, i)
    return time_func(run, number=runs)


def benchmark_insert_start_linkedlist(n: int, runs: int = 5) -> float:
    """Вставка n элементов в начало LinkedList (каждый insert O(1))."""
    def run() -> None:
        ll: LinkedList[int] = LinkedList()
        for i in range(n):
            ll.insert_at_start(i)
    return time_func(run, number=runs)


def benchmark_pop0_list(n: int, runs: int = 5) -> float:
    """Удаление из начала list pop(0) - O(n) на операцию."""
    def run() -> None:
        lst = list(range(n))
        for _ in range(n):
            lst.pop(0)
    return time_func(run, number=runs)


def benchmark_popleft_deque(n: int, runs: int = 5) -> float:
    """Удаление из начала deque.popleft() - O(1) на операцию."""
    def run() -> None:
        dq: deque = deque(range(n))
        for _ in range(n):
            dq.popleft()
    return time_func(run, number=runs)
