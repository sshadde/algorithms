"""Визуализация результатов тестирования."""
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any
import ast
import os


def load_results(
        filename: str = "report/sorting_results.txt"
                      ) -> Dict[str, Any]:
    """
    Загрузка результатов тестирования из файла.

    Args:
        filename: Имя файла с результатами

    Returns:
        Словарь с результатами тестирования
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден! Сначала запустите тесты.")
        return {}

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        results = ast.literal_eval(content)
        print(f"Загружены результаты тестирования из {filename}")
        return results

    except Exception as e:
        print(f"Ошибка при загрузке результатов: {e}")
        return {}


def plot_time_vs_size(results: Dict[str, Any], data_type: str = "random"):
    """
    Построение графиков зависимости времени выполнения от размера массива
    для каждого алгоритма на одном типе данных.

    Args:
        results: Результаты тестирования
        data_type: Тип данных ('random', 'sorted', 'reversed', 'almost_sorted')
    """
    if not results:
        print("Нет данных для построения графиков")
        return

    plt.figure(figsize=(12, 8))

    first_algo = next(iter(results.values()))
    sizes = sorted(list(first_algo[data_type].keys()))

    for algo_name, algo_data in results.items():
        times = []
        for size in sizes:
            time_val = algo_data[data_type].get(size, 0)
            times.append(time_val)

        plt.plot(sizes, times, marker='o', linewidth=2,
                 label=algo_name, markersize=6)

    plt.xlabel('Размер массива', fontsize=12)
    plt.ylabel('Время выполнения (сек)', fontsize=12)
    plt.title(
        f'Зависимость времени выполнения от размера '
        f'массива\n({data_type} данные)', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()

    os.makedirs('report', exist_ok=True)

    filename = f'report/time_vs_size_{data_type}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"График сохранен как {filename}")


def plot_time_vs_datatype(results: Dict[str, Any], size: int = 5000):
    """
    Построение графиков зависимости времени выполнения от типа данных
    для фиксированного размера массива.

    Args:
        results: Результаты тестирования
        size: Фиксированный размер массива
    """
    if not results:
        print("Нет данных для построения графиков")
        return

    plt.figure(figsize=(12, 8))

    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']

    algorithms = list(results.keys())
    x = np.arange(len(data_types))
    width = 0.15
    multiplier = 0

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, algo_name in enumerate(algorithms):
        times = []
        for data_type in data_types:
            time_val = results[algo_name][data_type].get(size, 0)
            times.append(time_val)

        offset = width * multiplier
        plt.bar(x + offset, times, width,
                label=algo_name, color=colors[i])
        multiplier += 1

    plt.xlabel('Тип данных', fontsize=12)
    plt.ylabel('Время выполнения (сек)', fontsize=12)
    plt.title(
        f'Сравнение времени выполнения '
        f'для размера массива {size}', fontsize=14)
    plt.xticks(x + width * 2, data_types, fontsize=10)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    os.makedirs('report', exist_ok=True)

    filename = f'report/time_vs_datatype_{size}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"График сохранен как {filename}")


if __name__ == "__main__":
    results = load_results()

    if results:
        print("Создание визуализаций...")
        plot_time_vs_size(results, "random")
        plot_time_vs_datatype(results, 5000)
    else:
        print("Не удалось загрузить результаты для визуализации")
