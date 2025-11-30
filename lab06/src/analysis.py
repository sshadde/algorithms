"""Анализ производительности."""
import time
import random
import matplotlib.pyplot as plt
from binary_search_tree import BinarySearchTree


def measure_search_time(tree: BinarySearchTree, values: list,
                        num_searches: int = 1000) -> float:
    """Измерение времени выполнения операций поиска."""
    start_time = time.perf_counter()

    for _ in range(num_searches):
        for value in values:
            tree.search(value)

    end_time = time.perf_counter()
    return end_time - start_time


def analyze_trees():
    """Анализ сбалансированного и вырожденного деревьев."""
    sizes = [100, 500, 1000, 2000, 5000]

    print("Анализ производительности BST")
    print("=" * 60)
    print("Размер дерева | Сбалансированное (сек) "
          "| Вырожденное (сек) | Отношение")
    print("-" * 80)

    results = []

    for size in sizes:
        balanced_tree = BinarySearchTree()
        random_values = random.sample(range(size * 10), size)
        for value in random_values:
            balanced_tree.insert(value)

        degenerate_tree = BinarySearchTree()
        sorted_values = list(range(size))
        for value in sorted_values:
            degenerate_tree.insert(value)

        test_values = random_values[:100] if len(
            random_values) >= 100 else random_values
        balanced_time = measure_search_time(balanced_tree, test_values)
        degenerate_time = measure_search_time(
            degenerate_tree, sorted_values[:100])
        ratio = degenerate_time / balanced_time if balanced_time > 0 else 0

        results.append({
            'size': size,
            'balanced': balanced_time,
            'degenerate': degenerate_time,
            'ratio': ratio
        })

        print(
            f"{size:12} | {balanced_time:19.4f} | "
            f"{degenerate_time:16.4f} | {ratio:8.2f}x")

    return results


def print_analysis(results):
    """Анализ результатов."""
    print("\n=== Анализ результатов ===")
    print("Теоретическая сложность:")
    print("- Сбалансированное дерево: O(log n)")
    print("- Вырожденное дерево: O(n)")
    print("\nПрактические результаты:")

    for result in results:
        print(f"Размер {result['size']}: "
              f"сбалансированное = {result['balanced']:.4f}с, "
              f"вырожденное = {result['degenerate']:.4f}с, "
              f"разница = {result['ratio']:.2f}x")

    avg_ratio = sum(r['ratio'] for r in results) / len(results)
    print(f"\nСредняя разница в производительности: {avg_ratio:.2f}x")


def plot_results(results):
    """Построение графиков результатов."""
    sizes = [r['size'] for r in results]
    balanced_times = [r['balanced'] for r in results]
    degenerate_times = [r['degenerate'] for r in results]

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, balanced_times, 'g-',
             label='Сбалансированное', marker='o', linewidth=2)
    plt.plot(sizes, degenerate_times, 'r-',
             label='Вырожденное', marker='s', linewidth=2)
    plt.xlabel('Размер дерева (количество элементов)')
    plt.ylabel('Время выполнения 1000 поисков (секунды)')
    plt.title('Сравнение времени поиска в BST')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    ratios = [r['ratio'] for r in results]
    plt.plot(sizes, ratios, 'b-', marker='o', linewidth=2)
    plt.xlabel('Размер дерева (количество элементов)')
    plt.ylabel('Отношение времени (вырожденное/сбалансированное)')
    plt.title('Отношение производительности')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('report/performance_comparison.png',
                dpi=300, bbox_inches='tight')
    print("\nГрафики сохранены в report/performance_comparison.png")


if __name__ == "__main__":
    results = analyze_trees()
    print_analysis(results)
    plot_results(results)
