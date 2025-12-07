"""Построение графиков зависимости времени выполнения от размера задачи"""
import time
import random
import matplotlib.pyplot as plt
from dynamic_programming import Fibonacci, Knapsack01, LCS, Levenshtein


def plot_fibonacci():
    """График для чисел Фибоначчи"""

    print("Фибоначчи: измеряем время...")

    sizes = list(range(10, 101, 10))
    times_naive = []
    times_dp = []

    for n in sizes:
        print(f"  n={n:3}: ", end="")

        if n <= 35:
            start = time.perf_counter()
            Fibonacci.naive_recursive(n)
            naive_time = time.perf_counter() - start
            times_naive.append(naive_time)
            print(f"наивная={naive_time:.6f}с, ", end="")
        else:
            times_naive.append(None)
            print("наивная=N/A, ", end="")

        start = time.perf_counter()
        Fibonacci.bottom_up(n)
        dp_time = time.perf_counter() - start
        times_dp.append(dp_time)
        print(f"ДП={dp_time:.6f}с")

    plt.figure(figsize=(10, 6))

    valid_indices = [i for i, t in enumerate(times_naive) if t is not None]
    valid_sizes = [sizes[i] for i in valid_indices]
    valid_times_naive = [times_naive[i] for i in valid_indices]

    plt.plot(valid_sizes, valid_times_naive, 'r-', linewidth=2,
             marker='o', label='Наивная рекурсия (O(2ⁿ))')
    plt.plot(sizes, times_dp, 'g-', linewidth=2,
             marker='s', label='ДП (восходящий, O(n))')

    plt.title('Числа Фибоначчи: время выполнения',
              fontsize=14, fontweight='bold')
    plt.xlabel('n (номер числа Фибоначчи)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')

    plt.savefig('report/fibonacci_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("График сохранен: report/fibonacci_graph.png")
    return sizes, times_naive, times_dp


def plot_knapsack():
    """График для задачи о рюкзаке"""

    print("\nРюкзак: измеряем время...")

    sizes = [5, 10, 15, 20, 25, 30, 35, 40]
    times = []
    results = []

    for n in sizes:
        weights = [random.randint(1, 20) for _ in range(n)]
        values = [random.randint(1, 50) for _ in range(n)]
        capacity = sum(weights) // 2

        start = time.perf_counter()
        result, _ = Knapsack01.bottom_up(weights, values, capacity)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        results.append(result)

        print(f"  n={n:2}: время={elapsed:.6f}с, результат={result}")

    plt.figure(figsize=(10, 6))

    plt.plot(sizes, times, 'b-', linewidth=2, marker='o')

    plt.title('Задача о рюкзаке 0-1: время выполнения',
              fontsize=14, fontweight='bold')
    plt.xlabel('Количество предметов (n)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.grid(True, alpha=0.3)

    for i, (x, y) in enumerate(zip(sizes, times)):
        plt.annotate(f'{y:.4f}с', (x, y), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=9)

    plt.savefig('report/knapsack_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("График сохранен: report/knapsack_graph.png")
    return sizes, times, results


def plot_lcs():
    """График для LCS"""

    print("\nLCS: измеряем время...")

    sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    times = []

    for n in sizes:
        str1 = ''.join(random.choices('ACGT', k=n))
        str2 = ''.join(random.choices('ACGT', k=n))

        start = time.perf_counter()
        LCS.bottom_up(str1, str2)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        print(f"  n={n:2}: время={elapsed:.6f}с")

    plt.figure(figsize=(10, 6))

    plt.plot(sizes, times, 'orange', linewidth=2, marker='s')

    plt.title('Наибольшая общая подпоследовательность: время выполнения',
              fontsize=14, fontweight='bold')
    plt.xlabel('Длина строк (n)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.grid(True, alpha=0.3)

    plt.savefig('report/lcs_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("График сохранен: report/lcs_graph.png")
    return sizes, times


def plot_levenshtein():
    """График для расстояния Левенштейна"""

    print("\nЛевенштейн: измеряем время...")

    sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    times = []

    for n in sizes:
        str1 = ''.join(random.choices('abcdefgh', k=n))
        str2 = ''.join(random.choices('abcdefgh', k=n))

        start = time.perf_counter()
        Levenshtein.bottom_up(str1, str2)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        print(f"  n={n:2}: время={elapsed:.6f}с")

    plt.figure(figsize=(10, 6))

    plt.plot(sizes, times, 'purple', linewidth=2, marker='^')

    plt.title('Расстояние Левенштейна: время выполнения',
              fontsize=14, fontweight='bold')
    plt.xlabel('Длина строк (n)', fontsize=12)
    plt.ylabel('Время (секунды)', fontsize=12)
    plt.grid(True, alpha=0.3)

    plt.savefig('report/levenshtein_graph.png',
                dpi=150, bbox_inches='tight')
    plt.close()

    print("График сохранен: report/levenshtein_graph.png")
    return sizes, times


def plot_comparison():
    """Сравнительный график всех алгоритмов"""

    print("\nСравнительный график: измеряем время...")

    sizes = [10, 20, 30, 40, 50]
    times_fib = []
    times_knap = []
    times_lcs = []
    times_lev = []

    for n in sizes:
        start = time.perf_counter()
        Fibonacci.bottom_up(n)
        times_fib.append(time.perf_counter() - start)

        weights = [random.randint(1, 10) for _ in range(n)]
        values = [random.randint(1, 20) for _ in range(n)]
        capacity = sum(weights) // 2

        start = time.perf_counter()
        Knapsack01.bottom_up(weights, values, capacity)
        times_knap.append(time.perf_counter() - start)

        str1 = ''.join(random.choices('AB', k=n))
        str2 = ''.join(random.choices('AB', k=n))

        start = time.perf_counter()
        LCS.bottom_up(str1, str2)
        times_lcs.append(time.perf_counter() - start)

        start = time.perf_counter()
        Levenshtein.bottom_up(str1, str2)
        times_lev.append(time.perf_counter() - start)

        print(f"  n={n}: Фибоначчи={times_fib[-1]:.6f}с, "
              f"Рюкзак={times_knap[-1]:.6f}с, "
              f"LCS={times_lcs[-1]:.6f}с, Левенштейн={times_lev[-1]:.6f}с")

    plt.figure(figsize=(12, 7))

    plt.plot(sizes, times_fib, 'r-', linewidth=2,
             marker='o', label='Фибоначчи O(n)')
    plt.plot(sizes, times_knap, 'g-', linewidth=2,
             marker='s', label='Рюкзак O(n·W)')
    plt.plot(sizes, times_lcs, 'b-', linewidth=2,
             marker='^', label='LCS O(n²)')
    plt.plot(sizes, times_lev, 'purple', linewidth=2,
             marker='d', label='Левенштейн O(n²)')

    plt.title('Сравнение времени выполнения алгоритмов ДП',
              fontsize=16, fontweight='bold')
    plt.xlabel('Размер задачи (n)', fontsize=14)
    plt.ylabel('Время (секунды)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.yscale('log')

    plt.savefig('report/comparison_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("График сохранен: report/comparison_graph.png")

    print("\n" + "="*80)
    print("ТАБЛИЦА ДАННЫХ ДЛЯ ГРАФИКОВ:")
    print("="*80)
    print("Размер | Фибоначчи   | Рюкзак      | LCS         | Левенштейн  ")
    print("-"*80)
    for i, n in enumerate(sizes):
        print(f"{n:6} | {times_fib[i]:.8f} | {times_knap[i]:.8f} | "
              f"{times_lcs[i]:.8f} | {times_lev[i]:.8f}")

    return sizes, times_fib, times_knap, times_lcs, times_lev


def main():
    """Основная функция для построения всех графиков"""

    fib_data = plot_fibonacci()
    knap_data = plot_knapsack()
    lcs_data = plot_lcs()
    lev_data = plot_levenshtein()
    comp_data = plot_comparison()

    print("\nГрафики успешно построены!")
    print("\nСозданные файлы в папке 'report/':")
    print("  - fibonacci_graph.png")
    print("  - knapsack_graph.png")
    print("  - lcs_graph.png")
    print("  - levenshtein_graph.png")
    print("  - comparison_graph.png")

    return {
        'fibonacci': fib_data,
        'knapsack': knap_data,
        'lcs': lcs_data,
        'levenshtein': lev_data,
        'comparison': comp_data
    }


if __name__ == "__main__":
    main()
