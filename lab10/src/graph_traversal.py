"""Алгоритмы обхода графов: BFS и DFS"""
from collections import deque
from typing import List, Dict
from graph_representation import AdjacencyList


def bfs(graph: AdjacencyList, start: int) -> Dict[int, int]:
    """
    Поиск в ширину (BFS)
    Сложность: O(V + E)
    Возвращает расстояния от стартовой вершины до всех достижимых
    """
    visited = [False] * graph.num_vertices
    distance = [-1] * graph.num_vertices
    queue = deque([start])

    visited[start] = True
    distance[start] = 0

    while queue:
        current = queue.popleft()

        for neighbor in graph.get_neighbors(current):
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)

    return {i: dist for i, dist in enumerate(distance) if dist != -1}


def dfs_recursive(graph: AdjacencyList, start: int) -> List[int]:
    """
    Поиск в глубину (рекурсивный)
    Сложность: O(V + E)
    Возвращает порядок обхода вершин
    """
    visited = [False] * graph.num_vertices
    result = []

    def _dfs(vertex: int) -> None:
        visited[vertex] = True
        result.append(vertex)

        for neighbor in graph.get_neighbors(vertex):
            if not visited[neighbor]:
                _dfs(neighbor)

    _dfs(start)
    return result


def dfs_iterative(graph: AdjacencyList, start: int) -> List[int]:
    """
    Поиск в глубину (итеративный)
    Сложность: O(V + E)
    Возвращает порядок обхода вершин
    """
    visited = [False] * graph.num_vertices
    stack = [start]
    result = []

    while stack:
        vertex = stack.pop()

        if not visited[vertex]:
            visited[vertex] = True
            result.append(vertex)

            for neighbor in reversed(graph.get_neighbors(vertex)):
                if not visited[neighbor]:
                    stack.append(neighbor)

    return result


def connected_components(graph: AdjacencyList) -> List[List[int]]:
    """
    Поиск компонент связности
    Сложность: O(V + E)
    Возвращает список компонент связности
    """
    visited = [False] * graph.num_vertices
    components = []

    for vertex in range(graph.num_vertices):
        if not visited[vertex]:
            component = []
            stack = [vertex]

            while stack:
                v = stack.pop()
                if not visited[v]:
                    visited[v] = True
                    component.append(v)

                    for neighbor in graph.get_neighbors(v):
                        if not visited[neighbor]:
                            stack.append(neighbor)

            components.append(component)

    return components
