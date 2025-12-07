"""Модуль с реализациями классических жадных алгоритмов."""
from dataclasses import dataclass
import heapq
from typing import Dict, List, Tuple, Optional
import itertools


def interval_scheduling(intervals: List[Tuple[int, int]]
                        ) -> List[Tuple[int, int]]:
    """Выбирает максимальное количество непересекающихся интервалов.

    Жадный выбор: сортируем по времени окончания и выбираем каждый следующий
    совместимый интервал.

    Время: O(n log n) из-за сортировки.

    Возвращает список выбранных интервалов в порядке выбора.
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    result: List[Tuple[int, int]] = []
    last_end = -float('inf')

    for (start, end) in sorted_intervals:
        if start >= last_end:
            result.append((start, end))
            last_end = end

    return result


def fractional_knapsack(values: List[float],
                        weights: List[float],
                        capacity: float
                        ) -> Tuple[float, List[Tuple[int, float]]]:
    """Дробный рюкзак.

    Жадный выбор: сортировка предметов по удельной стоимости (value/weight),
    брать по возрастанию.
    Возвращает максимальную стоимость и список (индекс, взятая доля от 0 до 1).

    Время: O(n log n).
    """
    assert len(values) == len(
        weights), 'Значения и веса должны иметь одинаковую длину'
    items = []
    for i, (v, w) in enumerate(zip(values, weights)):
        if w == 0:
            continue
        items.append((v / w, i, v, w))

    items.sort(key=lambda x: x[0], reverse=True)

    total_value = 0.0
    taken: List[Tuple[int, float]] = []

    for ratio, i, v, w in items:
        if capacity <= 0:
            break
        take = min(1.0, capacity / w)
        total_value += v * take
        capacity -= w * take
        taken.append((i, take))

    return total_value, taken


@dataclass
class HuffNode:
    """Узел дерева Хаффмана."""
    freq: int
    symbol: Optional[str] = None
    left: Optional['HuffNode'] = None
    right: Optional['HuffNode'] = None


def build_huffman_tree(frequencies: Dict[str, int]) -> Optional[HuffNode]:
    """Строит дерево Хаффмана и возвращает корень.

    Реализация: используем кучу с кортежами (freq, counter, node),
    чтобы избежать ошибок сравнения узлов при равных частотах.

    Время: O(n log n)
    """
    if not frequencies:
        return None

    heap = []
    counter = itertools.count()
    for sym, fr in frequencies.items():
        node = HuffNode(fr, sym)
        heap.append((fr, next(counter), node))
    heapq.heapify(heap)

    while len(heap) > 1:
        fr1, _, node1 = heapq.heappop(heap)
        fr2, _, node2 = heapq.heappop(heap)
        merged = HuffNode(fr1 + fr2, None, node1, node2)
        heapq.heappush(heap, (merged.freq, next(counter), merged))

    return heap[0][2]


def huffman_codes(frequencies: Dict[str, int]) -> Dict[str, str]:
    """Возвращает префиксные коды для символов в словаре частот.

    Построение дерева — через build_huffman_tree.
    Обходом Depth-First Search получаем коды.
    """
    root = build_huffman_tree(frequencies)
    codes: Dict[str, str] = {}

    def _dfs(node: Optional[HuffNode], prefix: str) -> None:
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = prefix or '0'
        else:
            _dfs(node.left, prefix + '0')
            _dfs(node.right, prefix + '1')

    _dfs(root, '')
    return codes


def coin_change_greedy(amount: int, coins: List[int]) -> List[int]:
    """Жадный алгоритм для выдачи сдачи: берет по наибольшему номиналу.

    Возвращает список количеств монет в том же порядке, что и coins.

    Время: O(n log n).
    """
    coins_sorted = sorted(coins, reverse=True)
    counts: Dict[int, int] = {c: 0 for c in coins_sorted}
    remaining = amount

    for c in coins_sorted:
        if remaining <= 0:
            break
        take = remaining // c
        counts[c] = take
        remaining -= take * c

    return [counts[c] for c in coins]


class UnionFind:
    """
    Структура данных для системы непересекающихся множеств.

    Используется в алгоритме Краскала для эффективной проверки связности.
    """

    def __init__(self, n: int) -> None:
        """Инициализирует Disjount Set Union для n элементов."""
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Находит представителя множества для элемента x со сжатием путей."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Объединяет множества, содержащие x и y."""
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        else:
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        return True


def kruskal_mst(num_vertices: int,
                edges: List[Tuple[int, int, float]]
                ) -> List[Tuple[int, int, float]]:
    """Реализация алгоритма Краскала для минимального остовного дерева.

    edges: список ребер (u, v, weight).
    Возвращает список ребер, входящих в MST.

    Время: O(n log n) из-за сортировки ребер.
    """
    uf = UnionFind(num_vertices)
    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst: List[Tuple[int, int, float]] = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == num_vertices - 1:
                break

    return mst


if __name__ == '__main__':
    """Демонстрация выполненных задач."""
    print('Примеры работы реализаций:')

    intervals_example = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9),
                         (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    print('\nInterval Scheduling:')
    print('Вход:', intervals_example)
    print('Выбранные интервалы:', interval_scheduling(intervals_example))

    values = [60.0, 100.0, 120.0]
    weights = [10.0, 20.0, 30.0]
    capacity = 50
    print('\nFractional Knapsack:')
    max_val, taken = fractional_knapsack(values, weights, capacity)
    print('Максимальное значение:', max_val)
    print('Взятое (index, fraction):', taken)

    freqs = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
    print('\nHuffman codes:')
    codes = huffman_codes(freqs)
    for s, code in codes.items():
        print(s, code)

    print('\nCoin change (greedy) для значения = 63 с монетами [25,10,5,1]:')
    print(coin_change_greedy(63, [25, 10, 5, 1]))

    print('\nKruskal MST пример:')
    edges = [(0, 1, 4.0), (0, 2, 3.0), (1, 2, 2.0), (1, 3, 5.0), (2, 3, 7.0)]
    print(kruskal_mst(4, edges))
