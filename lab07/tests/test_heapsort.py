"""Unit-тесты для функции heapsort."""
import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from heapsort import heapsort  # type: ignore  # noqa: E402


class TestHeapsort(unittest.TestCase):
    """Тестирование сортировки кучей."""

    def test_sort_ascending(self):
        """Тест сортировки по возрастанию."""
        arrays = [
            [9, 5, 2, 7, 1, 6],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [42],
            [3, 3, 3, 3],
            [3.5, 1.2, 4.7, 2.1],
        ]

        for arr in arrays:
            with self.subTest(arr=arr):
                original = arr.copy()
                heapsort(arr, ascending=True)

                for i in range(len(arr) - 1):
                    self.assertTrue(arr[i] <= arr[i + 1])

                self.assertEqual(sorted(original), arr)

    def test_sort_descending(self):
        """Тест сортировки по убыванию."""
        arrays = [
            [9, 5, 2, 7, 1, 6],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [42],
            [3, 3, 3, 3],
            [3.5, 1.2, 4.7, 2.1],
        ]

        for arr in arrays:
            with self.subTest(arr=arr):
                original = arr.copy()
                heapsort(arr, ascending=False)

                for i in range(len(arr) - 1):
                    self.assertTrue(arr[i] >= arr[i + 1])

                self.assertEqual(sorted(original, reverse=True), arr)

    def test_empty_array(self):
        """Тест сортировки пустого массива."""
        arr = []
        heapsort(arr)
        self.assertEqual(arr, [])

    def test_in_place(self):
        """Тест, что сортировка выполняется in-place."""
        arr = [9, 5, 2, 7, 1]
        original_id = id(arr)
        heapsort(arr)
        self.assertEqual(id(arr), original_id)


if __name__ == '__main__':
    unittest.main()
