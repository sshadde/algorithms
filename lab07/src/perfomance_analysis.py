"""Экспериментальное исследование производительности кучи и сортировок."""
import time
import random
import statistics
from typing import List, Callable, Tuple, Union
import matplotlib.pyplot as plt

from heap import Heap
from heapsort import heapsort


def measure_heap_construction(n: int, method: str = 'build_heap') -> float:
    """
    Замер времени построения кучи разными методами.

    Args:
        n: Количество элементов.
        method: 'build_heap' или 'insert'.

    Returns:
        Время в секундах.
    """
    data: List[Union[int, float]] = [random.randint(0, 10000)
                                     for _ in range(n)]
    heap = Heap(is_min=True)

    start = time.perf_counter()

    if method == 'build_heap':
        heap.build_heap(data)
    elif method == 'insert':
        for value in data:
            heap.insert(value)
    else:
        raise ValueError(f"Неизвестный метод: {method}")

    end = time.perf_counter()
    return end - start


def measure_sorting_time(n: int, sort_func: Callable, **kwargs) -> float:
    """
    Замер времени сортировки.

    Args:
        n: Количество элементов.
        sort_func: Функция сортировки.
        **kwargs: Дополнительные аргументы для sort_func.

    Returns:
        Время в секундах.
    """
    data = [random.randint(0, 10000) for _ in range(n)]

    start = time.perf_counter()
    sort_func(data, **kwargs)
    end = time.perf_counter()

    return end - start


def quicksort(arr: List[int]) -> List[int]:
    """Быстрая сортировка (рекурсивная реализация)."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)


def mergesort(arr: List[int]) -> List[int]:
    """Сортировка слиянием (рекурсивная реализация)."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Слияние двух отсортированных массивов."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def run_heap_construction_experiment() -> Tuple[List[int],
                                                List[float], List[float]]:
    """
    Эксперимент: сравнение методов построения кучи.

    Returns:
        (sizes, insert_times, build_heap_times)
    """
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    insert_times = []
    build_heap_times = []

    print("Эксперимент 1: Сравнение методов построения кучи")
    print("=" * 60)
    print(f"{'n':<10} {'insert (s)':<15} {'build_heap (s)':<15} "
          f"{'insert/build_heap':<15}")
    print("-" * 60)

    for n in sizes:
        insert_time = statistics.mean(
            [measure_heap_construction(n, 'insert') for _ in range(5)]
        )
        build_time = statistics.mean(
            [measure_heap_construction(n, 'build_heap') for _ in range(5)]
        )

        insert_times.append(insert_time)
        build_heap_times.append(build_time)

        ratio = insert_time / build_time if build_time > 0 else 0
        print(f"{n:<10} {insert_time:<15.6f} "
              f"{build_time:<15.6f} {ratio:<15.2f}")

    return sizes, insert_times, build_heap_times


def run_sorting_comparison_experiment() -> Tuple[List[int], List[float],
                                                 List[float], List[float]]:
    """
    Эксперимент: сравнение алгоритмов сортировки.

    Returns:
        (sizes, heapsort_times, quicksort_times, mergesort_times)
    """
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    heapsort_times = []
    quicksort_times = []
    mergesort_times = []

    print("\nЭксперимент 2: Сравнение алгоритмов сортировки")
    print("=" * 80)
    print(f"{'n':<10} {'heapsort (s)':<15} {'quicksort (s)':<15} "
          f"{'mergesort (s)':<15}")
    print("-" * 80)

    for n in sizes:
        heapsort_time = statistics.mean([
            measure_sorting_time(n, lambda arr: heapsort(
                arr.copy(), ascending=True))
            for _ in range(5)
        ])

        quicksort_time = statistics.mean([
            measure_sorting_time(n, lambda arr: quicksort(arr.copy()))
            for _ in range(5)
        ])

        mergesort_time = statistics.mean([
            measure_sorting_time(n, lambda arr: mergesort(arr.copy()))
            for _ in range(5)
        ])

        heapsort_times.append(heapsort_time)
        quicksort_times.append(quicksort_time)
        mergesort_times.append(mergesort_time)

        print(
            f"{n:<10} {heapsort_time:<15.6f} {quicksort_time:<15.6f} "
            f"{mergesort_time:<15.6f}")

    return sizes, heapsort_times, quicksort_times, mergesort_times


def plot_results(
    sizes: List[int],
    insert_times: List[float],
    build_heap_times: List[float],
    heapsort_times: List[float],
    quicksort_times: List[float],
    mergesort_times: List[float]
) -> None:
    """Построение графиков результатов экспериментов."""
    fig, axes = plt.subplots(2, figsize=(14, 10))

    axes[0].plot(sizes, insert_times, 'o-',
                 label='Последовательная вставка', linewidth=2)
    axes[0].plot(sizes, build_heap_times, 's-',
                 label='Алгоритм build_heap', linewidth=2)
    axes[0].set_xlabel('Количество элементов')
    axes[0].set_ylabel('Время (секунды)')
    axes[0].set_title('Построение кучи: insert vs build_heap')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(sizes, heapsort_times, 'o-', label='Heapsort', linewidth=2)
    axes[1].plot(sizes, quicksort_times, 's-',
                 label='Quicksort', linewidth=2)
    axes[1].plot(sizes, mergesort_times, '^-',
                 label='Mergesort', linewidth=2)
    axes[1].set_xlabel('Количество элементов')
    axes[1].set_ylabel('Время (секунды)')
    axes[1].set_title('Сравнение алгоритмов сортировки')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('report/performance_results.png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    sizes, insert_times, build_heap_times = run_heap_construction_experiment()

    sizes_sort, heapsort_times, quicksort_times, mergesort_times = (
        run_sorting_comparison_experiment()
    )
    plot_results(
        sizes, insert_times, build_heap_times,
        heapsort_times, quicksort_times, mergesort_times
    )
