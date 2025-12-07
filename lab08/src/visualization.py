"""Визуализация: дерево Хаффмана и график замеров времени."""
from typing import Dict, Tuple, List
import random
import time
import csv
import matplotlib.pyplot as plt
from greedy_algorithms import build_huffman_tree, huffman_codes


def time_huffman(n_values: List[int], repetitions: int = 5
                 ) -> List[Tuple[int, float]]:
    """
    Для каждого n в n_values сформировать рандомный словарь частот размера n.

    Возвращает список (n, avg_time_seconds).
    """
    results = []
    for n in n_values:
        freqs = {str(i): random.randint(1, 1000) for i in range(n)}
        t0 = time.time()
        for _ in range(repetitions):
            _ = huffman_codes(freqs)
        t1 = time.time()
        avg = (t1 - t0) / repetitions
        results.append((n, avg))
        print(f"n={n:6d} avg_time={avg:.6f}s")
    return results


def plot_timings(results: List[Tuple[int, float]],
                 out_png: str = "report/huffman_timings.png",
                 out_csv: str = "report/huffman_timings.csv") -> None:
    """Построение графика зависимости времени от n."""
    ns = [r[0] for r in results]
    times = [r[1] for r in results]

    with open(out_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["n", "avg_time_seconds"])
        for n, t in results:
            writer.writerow([n, t])
    print(f"Результаты сохранены в: {out_csv}")

    plt.figure(figsize=(8, 5))
    plt.plot(ns, times, marker='o')
    plt.xlabel("n")
    plt.ylabel("avg time (sec)")
    plt.title("Коды Хаффмана: avg time, n")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    print(f"Результаты сохранены в: {out_png}")


def visualize_huffman_tree(frequencies: Dict[str, int]):
    """Визуализация дерева Хаффмана."""

    build_huffman_tree(frequencies)
    codes = huffman_codes(frequencies)

    def build_consistent_tree():
        """Строит дерево, где 0 всегда идет влево, 1 всегда вправо."""
        class TreeNode:
            def __init__(self, freq=0, symbol=None):
                self.freq = freq
                self.symbol = symbol
                self.left = None
                self.right = None

        total_freq = sum(frequencies.values())
        new_root = TreeNode(total_freq)

        for symbol, code in codes.items():
            node = new_root
            for bit in code:
                if bit == '0':
                    if node.left is None:
                        node.left = TreeNode()
                    node = node.left
                else:
                    if node.right is None:
                        node.right = TreeNode()
                    node = node.right
            node.symbol = symbol
            node.freq = frequencies[symbol]

        def compute_freqs(node):
            if node is None:
                return 0
            if node.symbol:
                return node.freq

            left_freq = compute_freqs(node.left)
            right_freq = compute_freqs(node.right)
            node.freq = left_freq + right_freq
            return node.freq

        compute_freqs(new_root)
        return new_root

    consistent_root = build_consistent_tree()

    def print_tree(node, prefix="", is_left=True):
        if node is None:
            return ""

        result = ""

        if node.right:
            result += print_tree(node.right, prefix +
                                 ("│   " if is_left else "    "), False)

        if node.symbol:
            node_str = f"'{node.symbol}':{node.freq}"
        else:
            node_str = f"[{node.freq}]"

        if prefix == "":
            result += node_str + "\n"
        else:
            result += prefix + \
                ("└── " if is_left else "┌── ") + node_str + "\n"

        if node.left:
            result += print_tree(node.left, prefix +
                                 ("    " if is_left else "│   "), True)

        return result

    tree_str = print_tree(consistent_root)
    print(tree_str)

    print("-"*60)
    print("СООТВЕТСТВИЕ КОДОВ:")
    for symbol, code in sorted(codes.items()):
        print(f"'{symbol}' → {code}")


def demonstrate_huffman_examples():
    """Демонстрация работы алгоритма Хаффмана на разных примерах."""

    print(
        "\nПРИМЕР 1: Различные частоты "
        "{'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}")
    visualize_huffman_tree(
        {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5})

    print(
        "\nПРИМЕР 2: Сбалансированные частоты "
        "{'A': 10, 'B': 10, 'C': 10, 'D': 10}")
    visualize_huffman_tree({'A': 10, 'B': 10, 'C': 10, 'D': 10})

    print("\nПРИМЕР 3: Два символа {'X': 30, 'Y': 20}")
    visualize_huffman_tree({'X': 30, 'Y': 20})


def run_all_demo() -> None:
    """Строит дерево и делает замеры для n."""

    n_values = [100, 500, 1000, 2000, 5000]
    results = time_huffman(n_values, repetitions=3)
    plot_timings(results, "report/huffman_timings.png",
                 "report/huffman_timings.csv")

    demonstrate_huffman_examples()


if __name__ == "__main__":
    """Запуск всех методов визуализации."""
    run_all_demo()
