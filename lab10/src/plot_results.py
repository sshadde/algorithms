"""Экспериментальное исследование и визуализация результатов"""
from shortest_path import dijkstra
from graph_traversal import bfs, dfs_iterative
from graph_representation import AdjacencyMatrix, AdjacencyList
import time
import random
import matplotlib.pyplot as plt


def measure_operations_time():
    """Сравнение времени выполнения операций для разных представлений графов"""
    print("\n" + "="*60)
    print("СРАВНЕНИЕ ВРЕМЕНИ ОПЕРАЦИЙ")
    print("="*60)

    sizes = [50, 100, 200, 400, 800]
    density = 0.1

    add_edge_times_matrix = []
    add_edge_times_list = []
    get_neighbors_times_matrix = []
    get_neighbors_times_list = []

    for size in sizes:
        graph_matrix = AdjacencyMatrix(size)
        graph_list = AdjacencyList(size)

        start = time.time()
        for i in range(size):
            for j in range(int(size * density)):
                v = random.randint(0, size - 1)
                if i != v:
                    graph_matrix.add_edge(i, v)
        add_edge_times_matrix.append(time.time() - start)

        start = time.time()
        for i in range(size):
            for j in range(int(size * density)):
                v = random.randint(0, size - 1)
                if i != v:
                    graph_list.add_edge(i, v)
        add_edge_times_list.append(time.time() - start)

        start = time.time()
        for i in range(size):
            _ = graph_matrix.get_neighbors(i)
        get_neighbors_times_matrix.append(time.time() - start)

        start = time.time()
        for i in range(size):
            _ = graph_list.get_neighbors(i)
        get_neighbors_times_list.append(time.time() - start)

        print(f"Размер {size:3d}: "
              f"Матрица - добавление: {add_edge_times_matrix[-1]:.4f}с, "
              f"соседи: {get_neighbors_times_matrix[-1]:.4f}с | "
              f"Список - добавление: {add_edge_times_list[-1]:.4f}с, "
              f"соседи: {get_neighbors_times_list[-1]:.4f}с")

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, add_edge_times_matrix, 'r-', label='Матрица', marker='o')
    plt.plot(sizes, add_edge_times_list, 'b-', label='Список', marker='s')
    plt.xlabel('Количество вершин')
    plt.ylabel('Время (сек)')
    plt.title('Время добавления ребер')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, get_neighbors_times_matrix,
             'r-', label='Матрица', marker='o')
    plt.plot(sizes, get_neighbors_times_list, 'b-', label='Список', marker='s')
    plt.xlabel('Количество вершин')
    plt.ylabel('Время (сек)')
    plt.title('Время получения соседей')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('report/operations_comparison.png', dpi=300)

    return sizes, (add_edge_times_matrix, add_edge_times_list,
                   get_neighbors_times_matrix, get_neighbors_times_list)


def measure_algorithms_scalability():
    """Исследование масштабируемости алгоритмов на больших графах"""
    print("\n" + "="*60)
    print("МАСШТАБИРУЕМОСТЬ АЛГОРИТМОВ")
    print("="*60)

    sizes = [100, 200, 400, 800, 1600, 3200]
    densities = [0.05, 0.1, 0.2]

    bfs_results = {d: [] for d in densities}
    dfs_results = {d: [] for d in densities}

    for density in densities:
        print(f"\nПлотность графа: {density*100}%")

        for size in sizes:
            graph = AdjacencyList(size)
            edges_added = 0
            target_edges = int(size * (size - 1) / 2 * density)

            while edges_added < target_edges:
                u = random.randint(0, size - 1)
                v = random.randint(0, size - 1)
                if u != v and not graph.has_edge(u, v):
                    graph.add_edge(u, v)
                    edges_added += 1

            start = time.time()
            bfs(graph, 0)
            bfs_time = time.time() - start
            bfs_results[density].append(bfs_time)

            start = time.time()
            dfs_iterative(graph, 0)
            dfs_time = time.time() - start
            dfs_results[density].append(dfs_time)

            print(
                f"  Размер {size:4d}: BFS={bfs_time:.4f}с, "
                f"DFS={dfs_time:.4f}с")

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    for density in densities:
        plt.plot(sizes, bfs_results[density],
                 label=f'BFS (плотность={density})', marker='o')
    plt.xlabel('Количество вершин')
    plt.ylabel('Время (сек)')
    plt.title('Масштабируемость BFS')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    for density in densities:
        plt.plot(sizes, dfs_results[density],
                 label=f'DFS (плотность={density})', marker='s')
    plt.xlabel('Количество вершин')
    plt.ylabel('Время (сек)')
    plt.title('Масштабируемость DFS')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('report/algorithms_scalability.png', dpi=300)

    return sizes, bfs_results, dfs_results


def measure_dijkstra_complexity():
    """Замер времени выполнения алгоритма Дейкстры"""
    print("\n" + "="*60)
    print("СЛОЖНОСТЬ АЛГОРИТМА ДЕЙКСТРЫ")
    print("="*60)

    sizes = [50, 100, 200, 400, 800]
    results = []

    for size in sizes:
        graph = AdjacencyList(size, directed=True)

        for i in range(size):
            for j in range(5):
                v = random.randint(0, size - 1)
                if i != v:
                    weight = random.randint(1, 100)
                    graph.add_edge(i, v, weight)

        start = time.time()
        dijkstra(graph, 0)
        dijkstra_time = time.time() - start
        results.append(dijkstra_time)

        print(f"Размер {size:3d}: время Дейкстры = {dijkstra_time:.4f}с")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, results, 'g-', marker='^', linewidth=2)
    plt.xlabel('Количество вершин')
    plt.ylabel('Время (сек)')
    plt.title('Зависимость времени Дейкстры от размера графа')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('report/dijkstra_complexity.png', dpi=300)

    return sizes, results


def main():
    """Основная функция для запуска всех экспериментов"""
    print("\n" + "="*80)
    print("ЭКСПЕРИМЕНТАЛЬНОЕ ИССЛЕДОВАНИЕ АЛГОРИТМОВ НА ГРАФАХ")
    print("="*80)

    sizes_ops, ops_results = measure_operations_time()

    sizes_algo, bfs_results, dfs_results = measure_algorithms_scalability()

    sizes_dijk, dijkstra_results = measure_dijkstra_complexity()

    print("\n" + "="*80)
    print("Графики сохранены в папке 'report/'")
    print("="*80)

    with open('report/experimental_summary.txt', 'w', encoding='utf-8') as f:

        f.write("1. СРАВНЕНИЕ ОПЕРАЦИЙ (время в секундах):\n")
        f.write("-"*50 + "\n")
        f.write(
            "Размер | Матрица (доб.) | Список (доб.) | "
            "Матрица (сосед.) | Список (сосед.)\n")
        for i, size in enumerate(sizes_ops):
            f.write(f"{size:6d} | {ops_results[0][i]:14.4f} | "
                    f"{ops_results[1][i]:13.4f} | "
                    f"{ops_results[2][i]:17.4f} | "
                    f"{ops_results[3][i]:14.4f}\n")

        f.write("\n\n2. МАСШТАБИРУЕМОСТЬ АЛГОРИТМОВ (время в секундах):\n")
        f.write("-"*50 + "\n")
        f.write(
            "Размер | BFS(0.05) | DFS(0.05) | BFS(0.1) | "
            "DFS(0.1) | BFS(0.2) | DFS(0.2)\n")
        for i, size in enumerate(sizes_algo):
            f.write(f"{size:6d} | {bfs_results[0.05][i]:9.4f} | "
                    f"{dfs_results[0.05][i]:9.4f} | "
                    f"{bfs_results[0.1][i]:8.4f} | "
                    f"{dfs_results[0.1][i]:8.4f} | "
                    f"{bfs_results[0.2][i]:8.4f} | "
                    f"{dfs_results[0.2][i]:8.4f}\n")

        f.write("\n\n3. АЛГОРИТМ ДЕЙКСТРЫ:\n")
        f.write("-"*30 + "\n")
        f.write("Размер | Время (с)\n")
        for size, time_val in zip(sizes_dijk, dijkstra_results):
            f.write(f"{size:6d} | {time_val:10.4f}\n")


if __name__ == '__main__':
    random.seed(42)

    try:
        main()
    except KeyboardInterrupt:
        print("\nЭксперименты прерваны пользователем.")
    except Exception as e:
        print(f"\nОшибка: {e}")
