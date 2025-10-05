from __future__ import annotations
from collections import deque
from typing import Callable, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
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


def run_all_benchmarks(
    sizes: Optional[List[int]] = None, runs: int = 5
) -> Tuple[List[int], Dict[str, List[float]]]:
    """Запустить все бенчмарки по списку размеров.
    Возвращает кортеж (sizes, results), где results - словарь с
    измерениями в миллисекундах.
    """
    if sizes is None:
        sizes = [1000, 2000, 5000, 10000, 20000]

    results: Dict[str, List[float]] = {
        'list_insert0': [],
        'll_insert_start': [],
        'list_pop0': [],
        'deque_popleft': [],
    }

    for n in sizes:
        print(f'Running benchmarks for n={n} ...')
        results['list_insert0'].append(
            benchmark_insert_start_list(n, runs=runs)
        )
        results['ll_insert_start'].append(
            benchmark_insert_start_linkedlist(n, runs=runs)
        )
        results['list_pop0'].append(benchmark_pop0_list(n, runs=runs))
        results['deque_popleft'].append(
            benchmark_popleft_deque(n, runs=runs)
        )

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, results['list_insert0'], marker='o',
             label='list insert(0, x)')
    plt.plot(sizes, results['ll_insert_start'], marker='o',
             label='LinkedList insert_at_start')
    plt.xlabel('Размер (n)')
    plt.ylabel('Время (мс)')
    plt.title('Вставка в начало: list vs LinkedList')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.savefig(
        'results/insert_start_compare.png',
        dpi=300,
        bbox_inches='tight'
    )
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, results['list_pop0'], marker='o', label='list pop(0)')
    plt.plot(sizes, results['deque_popleft'], marker='o',
             label='deque popleft()')
    plt.xlabel('Размер (n)')
    plt.ylabel('Время (мс)')
    plt.title('Удаление из начала: list vs deque')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.savefig('results/pop0_vs_popleft.png', dpi=300,
                bbox_inches='tight')
    plt.close()

    return sizes, results


if __name__ == '__main__':
    import os
    os.makedirs('results', exist_ok=True)
    sizes, results = run_all_benchmarks(
        sizes=[1000, 2000, 5000, 10000], runs=3
    )
    print('Результаты сохранены в results.')
