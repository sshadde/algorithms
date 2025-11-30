import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple, Any
from hash_table_chaining import HashTableChaining
from hash_table_open_addressing import HashTableOpenAddressing
from hash_functions import simple_hash, polynomial_hash, djb2_hash


class PerformanceAnalyzer:
    def __init__(self):
        self.results = {}

    def generate_collision_test_data(self, n: int) -> List[Tuple[str, int]]:
        """
        Генерация тестовых данных, которые гарантированно создают коллизии.
        """

        test_data = []

        test_data.extend([
            ("ab", 1),
            ("ba", 2),
            ("ac", 3),
            ("ca", 4),
            ("bc", 5),
            ("cb", 6),
        ])

        for i in range(n - 6):
            test_data.append((f"key_{i}", i + 7))

        return test_data

    def count_collisions_chaining(self, table: HashTableChaining
                                  ) -> Dict[str, Any]:
        """Подсчет коллизий для метода цепочек."""
        collisions = 0
        max_chain_length = 0
        non_empty_buckets = 0

        for bucket in table.table:
            if len(bucket) > 0:
                non_empty_buckets += 1
                if len(bucket) > 1:
                    collisions += len(bucket) - 1
                max_chain_length = max(max_chain_length, len(bucket))

        return {
            'total_collisions': collisions,
            'max_chain_length': max_chain_length,
            'non_empty_buckets': non_empty_buckets,
            'load_factor': non_empty_buckets / table.size
        }

    def count_collisions_open_addressing(self, table: HashTableOpenAddressing,
                                         data_size: int) -> Dict[str, Any]:
        """Подсчет коллизий для открытой адресации"""
        probes_per_insert = []
        occupied_cells = 0

        test_data = self.generate_collision_test_data(data_size)

        for key, value in test_data:
            probe_count = 0
            for i in range(table.size):
                probe_count += 1
                index = table._probe_sequence(key, i)
                if (table.table[index] is None or
                        table.table[index][0] ==  # type: ignore
                        "__DELETED__"):
                    break
            probes_per_insert.append(probe_count)

        for cell in table.table:
            if cell is not None and cell[0] != "__DELETED__":
                occupied_cells += 1

        return {
            'avg_probes': np.mean(probes_per_insert) if probes_per_insert
            else 0,
            'max_probes': max(probes_per_insert) if probes_per_insert
            else 0,
            'occupied_cells': occupied_cells,
            'load_factor': occupied_cells / table.size
        }

    def measure_operations_chaining(self, hash_func, load_factor: float,
                                    data_size: int = 500):
        """Измерение производительности для метода цепочек"""
        table_size = max(int(data_size / load_factor), 10)
        table = HashTableChaining(size=table_size, hash_func=hash_func)
        test_data = self.generate_collision_test_data(data_size)

        start_time = time.perf_counter()
        for key, value in test_data:
            table.insert(key, value)
        insert_time = time.perf_counter() - start_time

        start_time = time.perf_counter()
        for key, value in test_data:
            table.search(key)
        search_time = time.perf_counter() - start_time

        collision_stats = self.count_collisions_chaining(table)

        return {
            'insert_time': insert_time / data_size * 1000,
            'search_time': search_time / data_size * 1000,
            'collisions': collision_stats['total_collisions'],
            'max_chain_length': collision_stats['max_chain_length'],
            'load_factor_actual': collision_stats['load_factor']
        }

    def measure_operations_open_addressing(self, probe_method: str, hash_func,
                                           load_factor: float,
                                           data_size: int = 500):
        """Измерение производительности для открытой адресации"""
        table_size = max(int(data_size / load_factor), 10)

        if load_factor > 0.8:
            table_size = int(data_size / 0.8)

        table = HashTableOpenAddressing(size=table_size,
                                        probe_method=probe_method,
                                        hash_func=hash_func)
        test_data = self.generate_collision_test_data(
            min(data_size, int(table_size * 0.8)))

        try:
            start_time = time.perf_counter()
            for key, value in test_data:
                table.insert(key, value)
            insert_time = time.perf_counter() - start_time

            start_time = time.perf_counter()
            for key, value in test_data:
                table.search(key)
            search_time = time.perf_counter() - start_time

            collision_stats = self.count_collisions_open_addressing(
                table, len(test_data))

            return {
                'insert_time': insert_time / len(test_data) * 1000,
                'search_time': search_time / len(test_data) * 1000,
                'avg_probes': collision_stats['avg_probes'],
                'max_probes': collision_stats['max_probes'],
                'load_factor_actual': collision_stats['load_factor'],
                'successful': True
            }

        except Exception as e:
            print(
                f"Ошибка при тестировании "
                f"{probe_method} с LF={load_factor}: {e}")
            return {
                'insert_time': float('inf'),
                'search_time': float('inf'),
                'avg_probes': 0,
                'max_probes': 0,
                'load_factor_actual': 0,
                'successful': False
            }

    def run_comparative_analysis(self):
        """Проведение сравнительного анализа"""
        print("Запуск сравнительного анализа производительности...")

        load_factors = [0.1, 0.3, 0.5, 0.7]
        hash_functions = [
            ('simple', simple_hash),
            ('polynomial', polynomial_hash),
            ('djb2', djb2_hash)
        ]

        print("\nАнализ метода цепочек...")
        for hash_name, hash_func in hash_functions:
            self.results[f'chaining_{hash_name}'] = {}
            for lf in load_factors:
                print(f"  Тестирование {hash_name} с LF={lf}...")
                result = self.measure_operations_chaining(hash_func, lf, 200)
                self.results[f'chaining_{hash_name}'][lf] = result
                if result['insert_time'] < float('inf'):
                    print(f"    ✓ Вставка: {result['insert_time']:.4f}мс, "
                          f"Коллизии: {result['collisions']}, "
                          f"Макс. цепочка: {result['max_chain_length']}")

        print("\nАнализ открытой адресации...")
        for probe_method in ['linear', 'double']:
            for hash_name, hash_func in hash_functions:
                key = f'open_{probe_method}_{hash_name}'
                self.results[key] = {}
                for lf in load_factors:
                    print(
                        f"  Тестирование {probe_method} {hash_name} "
                        f"с LF={lf}...")
                    result = self.measure_operations_open_addressing(
                        probe_method, hash_func, lf, 200)
                    self.results[key][lf] = result
                    if result['successful']:
                        print(f"    ✓ Вставка: {result['insert_time']:.4f}мс, "
                              f"Средние пробы: {result['avg_probes']:.2f}")
                    else:
                        print("    ✗ ПРОВАЛ")

    def plot_performance_comparison(self):
        """Построение графиков производительности"""
        load_factors = [0.1, 0.3, 0.5, 0.7]

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Сравнение производительности хеш-таблиц', fontsize=16)

        ax = axes[0, 0]
        for hash_name in ['simple', 'polynomial', 'djb2']:
            key = f'chaining_{hash_name}'
            times = []
            for lf in load_factors:
                if (lf in self.results[key]
                        and self.results[key][lf]['insert_time'] <
                        float('inf')):
                    times.append(self.results[key][lf]['insert_time'])
                else:
                    times.append(0)
            ax.plot(load_factors, times, marker='o', linewidth=2, markersize=8,
                    label=f'Цепочки {hash_name}')
        ax.set_title('Метод цепочек - Время вставки', fontsize=12)
        ax.set_xlabel('Коэффициент заполнения')
        ax.set_ylabel('Время на операцию (мс)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        for hash_name in ['simple', 'polynomial', 'djb2']:
            key = f'chaining_{hash_name}'
            times = []
            for lf in load_factors:
                if (lf in self.results[key]
                        and self.results[key][lf]['search_time'] <
                        float('inf')):
                    times.append(self.results[key][lf]['search_time'])
                else:
                    times.append(0)
            ax.plot(load_factors, times, marker='s', linewidth=2, markersize=8,
                    label=f'Цепочки {hash_name}')
        ax.set_title('Метод цепочек - Время поиска', fontsize=12)
        ax.set_xlabel('Коэффициент заполнения')
        ax.set_ylabel('Время на операцию (мс)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        for probe_method in ['linear', 'double']:
            for hash_name in ['djb2']:
                key = f'open_{probe_method}_{hash_name}'
                times = []
                for lf in load_factors:
                    if (lf in self.results[key]
                            and self.results[key][lf]['successful']
                            and self.results[key][lf]['insert_time'] <
                            float('inf')):
                        times.append(self.results[key][lf]['insert_time'])
                    else:
                        times.append(0)
                ax.plot(load_factors, times, marker='^',
                        linewidth=2, markersize=8,
                        label=f'Открытая {probe_method} {hash_name}')
        ax.set_title('Открытая адресация - Время вставки', fontsize=12)
        ax.set_xlabel('Коэффициент заполнения')
        ax.set_ylabel('Время на операцию (мс)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 1]
        for probe_method in ['linear', 'double']:
            for hash_name in ['djb2']:
                key = f'open_{probe_method}_{hash_name}'
                times = []
                for lf in load_factors:
                    if (lf in self.results[key]
                            and self.results[key][lf]['successful']
                            and self.results[key][lf]['search_time'] <
                            float('inf')):
                        times.append(self.results[key][lf]['search_time'])
                    else:
                        times.append(0)
                ax.plot(load_factors, times, marker='v',
                        linewidth=2, markersize=8,
                        label=f'Открытая {probe_method} {hash_name}')
        ax.set_title('Открытая адресация - Время поиска', fontsize=12)
        ax.set_xlabel('Коэффициент заполнения')
        ax.set_ylabel('Время на операцию (мс)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('report/performance_comparison.png', dpi=300,
                    bbox_inches='tight')

    def plot_collision_histograms(self):
        """Построение гистограмм коллизий"""
        load_factors = [0.1, 0.3, 0.5, 0.7]

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Коллизии в хеш-таблицах (метод цепочек)', fontsize=16)

        for i, lf in enumerate(load_factors):
            ax = axes[i // 2, i % 2]

            hash_names = ['simple', 'polynomial', 'djb2']
            collisions = []

            for hash_name in hash_names:
                key = f'chaining_{hash_name}'
                if lf in self.results[key]:
                    collisions.append(self.results[key][lf]['collisions'])
                else:
                    collisions.append(0)

            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
            bars = ax.bar(hash_names, collisions, color=colors, alpha=0.8)
            ax.set_title(f'Коэффициент заполнения = {lf}', fontsize=12)
            ax.set_ylabel('Количество коллизий')
            ax.set_ylim(0, max(collisions) *
                        1.2 if max(collisions) > 0 else 10)
            ax.grid(True, alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(height)}', ha='center', va='bottom',
                        fontweight='bold')

        plt.tight_layout()
        plt.savefig('report/collision_histograms.png', dpi=300,
                    bbox_inches='tight')


if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    analyzer.run_comparative_analysis()
    analyzer.plot_performance_comparison()
    analyzer.plot_collision_histograms()
