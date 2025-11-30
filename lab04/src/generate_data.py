"""Генерация случайных массивов."""
import random
from typing import Dict, List, Optional


def generate_random_array(size: int) -> List[int]:
    """Генерация случайного массива."""
    return [random.randint(0, 10000) for _ in range(size)]


def generate_sorted_array(size: int) -> List[int]:
    """Генерация отсортированного массива."""
    return list(range(size))


def generate_reversed_array(size: int) -> List[int]:
    """Генерация массива, отсортированного в обратном порядке."""
    return list(range(size, 0, -1))


def generate_almost_sorted_array(size: int) -> List[int]:
    """Генерация почти отсортированного массива (до 5% перемешано)."""
    arr = list(range(size))

    num_shuffled = max(1, size // 20)
    for _ in range(num_shuffled):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_test_data(
        sizes: Optional[List[int]] = None
        ) -> Dict[str, Dict[int, List[int]]]:
    """Генерация всех типов тестовых данных для различных размеров."""
    if sizes is None:
        sizes = [100, 1000, 5000, 10000]

    data_types = {
        'random': generate_random_array,
        'sorted': generate_sorted_array,
        'reversed': generate_reversed_array,
        'almost_sorted': generate_almost_sorted_array
    }

    test_data = {}  # type: ignore
    for data_type, generator in data_types.items():
        test_data[data_type] = {}
        for size in sizes:
            test_data[data_type][size] = generator(size)

    return test_data
