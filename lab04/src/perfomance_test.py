"""Тестирование алгоритмов сортировки"""
import timeit
import copy
import os
from typing import List, Dict, Any, Callable
from generate_data import generate_test_data
from sorts import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    is_sorted
)


def test_sorting_algorithm(algorithm: Callable, arr: List[int]) -> float:
    """
    Тестирование времени выполнения алгоритма сортировки.

    Args:
        algorithm: Функция сортировки
        arr: Массив для сортировки

    Returns:
        Время выполнения в секундах
    """
    test_arr = copy.deepcopy(arr)

    def sort_wrapper():
        return algorithm(test_arr)

    timer = timeit.Timer(sort_wrapper)

    if len(arr) >= 1000:
        execution_time = timer.timeit(number=1)
    else:
        execution_time = min(timer.repeat(repeat=3, number=1))

    return execution_time


def run_performance_tests() -> Dict[str, Dict[str, Dict[int, float]]]:
    """Запуск тестов производительности для всех алгоритмов и типов данных."""
    sizes = [100, 1000, 5000, 10000]
    test_data = generate_test_data(sizes)

    algorithms = {
        'bubble_sort': bubble_sort,
        'selection_sort': selection_sort,
        'insertion_sort': insertion_sort,
        'merge_sort': merge_sort,
        'quick_sort': quick_sort
    }

    results = {}  # type: ignore

    for algo_name, algorithm in algorithms.items():
        print(f"Тестирование {algo_name}...")
        results[algo_name] = {}

        for data_type, size_data in test_data.items():
            results[algo_name][data_type] = {}

            for size, arr in size_data.items():
                print(f"  Размер: {size}, тип: {data_type}")
                time_taken = test_sorting_algorithm(algorithm, arr)
                results[algo_name][data_type][size] = time_taken

                sorted_arr = algorithm(copy.deepcopy(arr))
                if not is_sorted(sorted_arr):
                    print(
                        f"ВНИМАНИЕ: {algo_name} "
                        f"некорректно отсортировал массив!"
                    )

    return results


def save_results_visual(results: Dict[str, Any],
                        filename: str = "report/sorting_results.txt"):
    """
    Сохранение результатов в формате, пригодном для визуализации.

    Args:
        results: Результаты тестирования
        filename: Имя файла для сохранения
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(results))


def create_summary_table(results: Dict[str, Any]) -> str:
    """
    Создание сводной таблицы результатов.

    Args:
        results: Результаты тестирования

    Returns:
        Текст таблицы в формате строки
    """
    if not results:
        return "Нет данных для создания таблицы"

    table = "СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ\n"
    table += "=" * 80 + "\n\n"

    sizes = [100, 1000, 5000, 10000]
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    algorithms = list(results.keys())

    for data_type in data_types:
        table += f"{data_type.upper()} ДАННЫЕ:\n"
        table += "-" * 60 + "\n"
        table += "Алгоритм".ljust(15)
        for size in sizes:
            table += f"{size:>8} эл."
        table += "\n" + "-" * 60 + "\n"

        for algo_name in algorithms:
            table += algo_name.ljust(20)
            for size in sizes:
                time_val = results[algo_name][data_type].get(size, 0)
                if time_val < 0.001:
                    table += f"{time_val:>10.6f}"
                elif time_val < 1:
                    table += f"{time_val:>10.4f}"
                else:
                    table += f"{time_val:>10.2f}"
            table += "\n"
        table += "\n"

    return table


if __name__ == "__main__":
    print("Запуск тестов производительности...")
    results = run_performance_tests()

    save_results_visual(results, "report/sorting_results.txt")

    summary = create_summary_table(results)
    with open("report/summary_table.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("\nРезультаты сохранены в папке report/")
    print("- sorting_results.txt - результаты для визуализации")
    print("- summary_table.txt - сводная таблица")
