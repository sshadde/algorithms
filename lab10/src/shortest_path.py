"""Алгоритмы для работы с графами: Дейкстра и топологическая сортировка"""
import heapq
from typing import List, Dict, Optional
from collections import deque
from graph_representation import AdjacencyList


def dijkstra(graph: AdjacencyList, start: int) -> Dict[int, int]:
    """
    Алгоритм Дейкстры для поиска кратчайших путей
    Работает только с неотрицательными весами
    Сложность: O((V + E) * log V) с использованием кучи
    """
    distances = [10**10] * graph.num_vertices
    distances[start] = 0
    visited = [False] * graph.num_vertices

    pq = [(0, start)]

    while pq:
        current_dist, current = heapq.heappop(pq)

        if visited[current]:
            continue

        visited[current] = True

        for neighbor in graph.get_neighbors(current):
            weight = graph.get_weight(current, neighbor)
            if weight is not None:
                distance = current_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

    return {i: dist for i, dist in enumerate(distances) if dist != 10**10}


def topological_sort(graph: AdjacencyList) -> Optional[List[int]]:
    """
    Топологическая сортировка для ориентированных ациклических графов (DAG)
    Использует алгоритм Кана (удаление вершин без входящих ребер)
    Сложность: O(V + E)
    """
    if not graph.directed:
        return None

    in_degree = [0] * graph.num_vertices
    for u in range(graph.num_vertices):
        for v in graph.get_neighbors(u):
            in_degree[v] += 1

    queue = deque([v for v in range(graph.num_vertices) if in_degree[v] == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)

        for v in graph.get_neighbors(u):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(result) != graph.num_vertices:
        return None

    return result
