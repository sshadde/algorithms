"""Примеры решения практических задач на графах"""
from typing import List, Tuple
from graph_representation import AdjacencyList
from graph_traversal import bfs, connected_components
from shortest_path import topological_sort


def maze_shortest_path(maze: List[List[int]], start: Tuple[int, int],
                       end: Tuple[int, int]) -> int:
    """
    Задача 1: Кратчайший путь в лабиринте
    0 - проход, 1 - стена
    Возвращает длину кратчайшего пути
    """
    rows, cols = len(maze), len(maze[0])

    def to_vertex(r: int, c: int) -> int:
        return r * cols + c

    num_vertices = rows * cols
    graph = AdjacencyList(num_vertices)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                        graph.add_edge(to_vertex(r, c), to_vertex(nr, nc))

    start_vertex = to_vertex(*start)
    end_vertex = to_vertex(*end)

    distances = bfs(graph, start_vertex)
    return distances.get(end_vertex, -1)


def network_connectivity(graph: AdjacencyList) -> int:
    """
    Задача 2: Определение связности сети
    Возвращает количество компонент связности
    """
    components = connected_components(graph)
    return len(components)


def task_scheduling(tasks: List[Tuple[str, List[str]]]) -> List[str]:
    """
    Задача 3: Топологическая сортировка задач
    tasks: список (задача, [зависимости])
    Возвращает порядок выполнения задач
    """
    task_names = list({task for task, _ in tasks})
    name_to_index = {name: i for i, name in enumerate(task_names)}

    graph = AdjacencyList(len(task_names), directed=True)

    for task, deps in tasks:
        task_idx = name_to_index[task]
        for dep in deps:
            dep_idx = name_to_index[dep]
            graph.add_edge(dep_idx, task_idx)

    order_indices = topological_sort(graph)
    if order_indices is None:
        raise ValueError("Обнаружен цикл в зависимостях!")

    return [task_names[i] for i in order_indices]
