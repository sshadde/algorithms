"""Запуск практических примеров"""
from graph_representation import AdjacencyList
from examples import (
    maze_shortest_path,
    network_connectivity,
    task_scheduling
)


def example_1_maze():
    """Пример 1: Лабиринт"""
    print("\n" + "="*50)
    print("Пример 1: Кратчайший путь в лабиринте")
    print("="*50)

    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    end = (4, 4)

    distance = maze_shortest_path(maze, start, end)

    print(f"\nСтарт: {start}")
    print(f"Финиш: {end}")
    print(f"Длина кратчайшего пути: {distance}")

    if distance > 0:
        print("Путь существует!")
    else:
        print("Путь не найден!")


def example_2_network():
    """Пример 2: Связность сети"""
    print("\n" + "="*50)
    print("Пример 2: Проверка связности сети")
    print("="*50)

    graph = AdjacencyList(8)

    connections = [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7)]
    for u, v in connections:
        graph.add_edge(u, v)

    num_components = network_connectivity(graph)

    print("Сеть состоит из следующих соединений:")
    for u, v in connections:
        print(f"Узел {u} соединен с узлом {v}")

    print(f"\nКоличество компонент связности: {num_components}")

    if num_components == 1:
        print("Сеть полностью связна!")
    else:
        print(f"Сеть разделена на {num_components} независимых подсетей.")


def example_3_tasks():
    """Пример 3: Планирование задач"""
    print("\n" + "="*50)
    print("Пример 3: Топологическая сортировка задач")
    print("="*50)

    tasks = [
        ("изучить теорию", []),
        ("написать код", ["изучить теорию"]),
        ("написать тесты", ["написать код"]),
        ("протестировать", ["написать тесты"]),
        ("написать отчет", ["протестировать", "изучить теорию"]),
        ("сдать работу", ["написать отчет"])
    ]

    try:
        order = task_scheduling(tasks)

        print("Задачи и их зависимости:")
        for task, deps in tasks:
            if deps:
                print(f"• {task} зависит от: {', '.join(deps)}")
            else:
                print(f"• {task} не имеет зависимостей")

        print("\nПорядок выполнения:")
        for i, task in enumerate(order, 1):
            print(f"{i}. {task}")

    except ValueError as e:
        print(f"Ошибка: {e}")


def example_4_dijkstra():
    """Пример 4: Маршрутизация"""
    print("\n" + "="*50)
    print("Пример 4: Поиск кратчайшего пути (Дейкстра)")
    print("="*50)

    graph = AdjacencyList(6, directed=True)

    roads = [
        (0, 1, 5),
        (0, 2, 2),
        (1, 2, 1),
        (1, 3, 3),
        (2, 1, 4),
        (2, 3, 8),
        (2, 4, 10),
        (3, 4, 2),
        (3, 5, 6),
        (4, 5, 3)
    ]

    cities = ["A", "B", "C", "D", "E", "F"]

    for u, v, w in roads:
        graph.add_edge(u, v, w)

    from shortest_path import dijkstra

    start_city = 0
    distances = dijkstra(graph, start_city)

    print("Дорожная сеть:")
    for u, v, w in roads:
        print(f"{cities[u]} → {cities[v]}: {w} км")

    print(f"\nКратчайшие расстояния из города {cities[start_city]}:")
    for city_idx, distance in distances.items():
        if city_idx != start_city:
            print(f"До города {cities[city_idx]}: {distance} км")

    farthest = max(distances.items(),
                   key=lambda x: x[1] if x[0] != start_city else 0)
    print(f"\nСамый дальний город: {cities[farthest[0]]} ({farthest[1]} км)")


if __name__ == '__main__':
    example_1_maze()
    example_2_network()
    example_3_tasks()
    example_4_dijkstra()
