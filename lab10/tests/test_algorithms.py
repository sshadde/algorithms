"""Тестирование алгоритмов на графах"""
import unittest
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from shortest_path import (   # type: ignore  # noqa: E402
    dijkstra, topological_sort
)
from graph_traversal import (  # type: ignore  # noqa: E402
    bfs, dfs_recursive, dfs_iterative, connected_components
)
from graph_representation import (  # type: ignore  # noqa: E402
    AdjacencyMatrix, AdjacencyList
)


class TestGraphAlgorithms(unittest.TestCase):

    def setUp(self):
        """Создание тестовых графов"""
        self.graph_list = AdjacencyList(5)
        self.graph_list.add_edge(0, 1)
        self.graph_list.add_edge(0, 2)
        self.graph_list.add_edge(1, 3)
        self.graph_list.add_edge(2, 4)

        self.graph_matrix = AdjacencyMatrix(5)
        self.graph_matrix.add_edge(0, 1)
        self.graph_matrix.add_edge(0, 2)
        self.graph_matrix.add_edge(1, 3)
        self.graph_matrix.add_edge(2, 4)

        self.dag = AdjacencyList(6, directed=True)
        self.dag.add_edge(5, 2)
        self.dag.add_edge(5, 0)
        self.dag.add_edge(4, 0)
        self.dag.add_edge(4, 1)
        self.dag.add_edge(2, 3)
        self.dag.add_edge(3, 1)

    def test_bfs(self):
        """Тест BFS"""
        distances = bfs(self.graph_list, 0)
        expected = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2}
        self.assertEqual(distances, expected)

    def test_dfs(self):
        """Тест DFS"""
        recursive = dfs_recursive(self.graph_list, 0)
        iterative = dfs_iterative(self.graph_list, 0)
        self.assertEqual(set(recursive), {0, 1, 2, 3, 4})
        self.assertEqual(set(iterative), {0, 1, 2, 3, 4})

    def test_connected_components(self):
        """Тест компонент связности"""
        graph = AdjacencyList(6)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(3, 4)
        graph.add_edge(4, 5)

        components = connected_components(graph)
        self.assertEqual(len(components), 2)

    def test_dijkstra(self):
        """Тест алгоритма Дейкстры"""
        graph = AdjacencyList(5, directed=True)
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 3)
        graph.add_edge(1, 2, 1)
        graph.add_edge(1, 3, 2)
        graph.add_edge(2, 1, 4)
        graph.add_edge(2, 3, 8)
        graph.add_edge(2, 4, 2)
        graph.add_edge(3, 4, 7)
        graph.add_edge(4, 3, 9)

        distances = dijkstra(graph, 0)
        self.assertEqual(distances[4], 5)

    def test_topological_sort(self):
        """Тест топологической сортировки"""
        order = topological_sort(self.dag)
        if order:
            for u in range(self.dag.num_vertices):
                for v in self.dag.get_neighbors(u):
                    self.assertLess(order.index(u), order.index(v))


class PerformanceTest(unittest.TestCase):
    """Тестирование производительности"""

    def test_performance_comparison(self):
        """Сравнение производительности матрицы и списка"""
        sizes = [10, 50, 100, 200]

        for size in sizes:
            print(f"\nТест графа размером {size} вершин:")

            start = time.time()
            graph_matrix = AdjacencyMatrix(size)
            for i in range(size):
                for j in range(i + 1, min(i + 10, size)):
                    graph_matrix.add_edge(i, j)
            matrix_time = time.time() - start

            start = time.time()
            graph_list = AdjacencyList(size)
            for i in range(size):
                for j in range(i + 1, min(i + 10, size)):
                    graph_list.add_edge(i, j)
            list_time = time.time() - start

            print(f"Матрица: {matrix_time:.6f} сек")
            print(f"Список: {list_time:.6f} сек")

            if list_time > 0.000001:
                print(
                    f"Отношение (матрица/список): {matrix_time/list_time:.2f}")
            else:
                print("Отношение: время слишком мало для точного сравнения")

            matrix_memory = size * size
            list_memory = size * 10 * 2
            print(f"Память матрицы (элементов): {matrix_memory}")
            print(f"Память списка (оценка): {list_memory}")
            print(
                f"Отношение памяти (матрица/список): "
                f"{matrix_memory/list_memory:.1f}")


def run_complexity_analysis():
    """Анализ сложности на больших графах"""
    print("\n" + "="*50)
    print("АНАЛИЗ СЛОЖНОСТИ АЛГОРИТМОВ")
    print("="*50)

    size = 500
    print(f"\nСоздание графа из {size} вершин...")

    start = time.time()
    graph_list = AdjacencyList(size)
    for i in range(size):
        for j in range(i + 1, min(i + 5, size)):
            graph_list.add_edge(i, j, weight=i+j)
    creation_time = time.time() - start
    print(f"Время создания графа: {creation_time:.4f} сек")

    start = time.time()
    bfs(graph_list, 0)
    bfs_time = time.time() - start
    print(f"Время BFS: {bfs_time:.6f} сек")

    start = time.time()
    dfs_iterative(graph_list, 0)
    dfs_time = time.time() - start
    print(f"Время DFS: {dfs_time:.6f} сек")

    start = time.time()
    dijkstra(graph_list, 0)
    dijkstra_time = time.time() - start
    print(f"Время Дейкстры: {dijkstra_time:.6f} сек")

    print("\nОтношения времени:")
    print(f"Дейкстра/BFS: {dijkstra_time/bfs_time:.2f}")
    print(f"DFS/BFS: {dfs_time/bfs_time:.2f}")


if __name__ == '__main__':
    print("ЗАПУСК UNIT-ТЕСТОВ")
    print("="*50)
    unittest.main(verbosity=2, exit=False)

    run_complexity_analysis()
