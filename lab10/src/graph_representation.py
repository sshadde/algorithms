"""Представления графов: матрица смежности и список смежности"""
from typing import Dict, List, Optional


class AdjacencyMatrix:
    """
    Граф на основе матрицы смежности.
    Память: O(V²) где V - количество вершин
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Добавление ребра между вершинами u и v
        Сложность: O(1)
        """
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.matrix[u][v] = weight
            if not self.directed:
                self.matrix[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """Удаление ребра - O(1)"""
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.matrix[u][v] = 0
            if not self.directed:
                self.matrix[v][u] = 0

    def get_neighbors(self, vertex: int) -> List[int]:
        """
        Получение соседей вершины
        Сложность: O(V) - нужно пройти всю строку
        """
        neighbors = []
        for v in range(self.num_vertices):
            if self.matrix[vertex][v] != 0:
                neighbors.append(v)
        return neighbors

    def has_edge(self, u: int, v: int) -> bool:
        """Проверка наличия ребра - O(1)"""
        return self.matrix[u][v] != 0

    def __str__(self) -> str:
        """Визуализация матрицы"""
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])


class AdjacencyList:
    """
    Граф на основе списка смежности.
    Память: O(V + E) где V - вершины, E - ребра
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.adj_list: List[Dict[int, int]] = [{} for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Добавление ребра между вершинами u и v
        Сложность: O(1)
        """
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.adj_list[u][v] = weight
            if not self.directed:
                self.adj_list[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """Удаление ребра - O(1) в среднем"""
        if v in self.adj_list[u]:
            del self.adj_list[u][v]
            if not self.directed:
                del self.adj_list[v][u]

    def get_neighbors(self, vertex: int) -> List[int]:
        """
        Получение соседей вершины
        Сложность: O(deg(v)) где deg(v) - степень вершины
        """
        return list(self.adj_list[vertex].keys())

    def has_edge(self, u: int, v: int) -> bool:
        """Проверка наличия ребра - O(1) в среднем"""
        return v in self.adj_list[u]

    def get_weight(self, u: int, v: int) -> Optional[int]:
        """Получение веса ребра - O(1) в среднем"""
        return self.adj_list[u].get(v)

    def __str__(self) -> str:
        """Визуализация списка смежности"""
        result = []
        for i in range(self.num_vertices):
            neighbors = ', '.join(
                [f'{v}({w})' for v, w in self.adj_list[i].items()])
            result.append(
                f'{i}: {neighbors}' if neighbors else f'{i}: нет соседей')
        return '\n'.join(result)
