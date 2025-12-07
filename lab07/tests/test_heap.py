"""Unit-тесты для класса Heap."""
import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from heap import Heap  # type: ignore # noqa: E402


class TestHeap(unittest.TestCase):
    """Тестирование кучи (min-heap и max-heap)."""

    def test_min_heap_insert_extract(self):
        """Тест вставки и извлечения из min-heap."""
        heap = Heap(is_min=True)
        heap.insert(5)
        heap.insert(3)
        heap.insert(8)
        heap.insert(1)

        self.assertEqual(heap.extract(), 1)
        self.assertEqual(heap.extract(), 3)
        self.assertEqual(heap.extract(), 5)
        self.assertEqual(heap.extract(), 8)
        with self.assertRaises(IndexError):
            heap.extract()

    def test_max_heap_insert_extract(self):
        """Тест вставки и извлечения из max-heap."""
        heap = Heap(is_min=False)
        heap.insert(5)
        heap.insert(3)
        heap.insert(8)
        heap.insert(1)

        self.assertEqual(heap.extract(), 8)
        self.assertEqual(heap.extract(), 5)
        self.assertEqual(heap.extract(), 3)
        self.assertEqual(heap.extract(), 1)
        with self.assertRaises(IndexError):
            heap.extract()

    def test_peek(self):
        """Тест просмотра корня без извлечения."""
        heap = Heap(is_min=True)
        self.assertIsNone(heap.peek())

        heap.insert(10)
        heap.insert(5)
        self.assertEqual(heap.peek(), 5)
        heap.extract()
        self.assertEqual(heap.peek(), 10)

    def test_build_heap_min(self):
        """Тест построения min-heap из массива."""
        array = [9, 5, 2, 7, 1, 6]
        heap = Heap(is_min=True)
        heap.build_heap(array)

        for i in range(len(heap.heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(heap.heap):
                self.assertTrue(heap.heap[i] <= heap.heap[left])
            if right < len(heap.heap):
                self.assertTrue(heap.heap[i] <= heap.heap[right])

        extracted = []
        while len(heap) > 0:
            extracted.append(heap.extract())
        self.assertEqual(extracted, [1, 2, 5, 6, 7, 9])

    def test_build_heap_max(self):
        """Тест построения max-heap из массива."""
        array = [9, 5, 2, 7, 1, 6]
        heap = Heap(is_min=False)
        heap.build_heap(array)

        for i in range(len(heap.heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(heap.heap):
                self.assertTrue(heap.heap[i] >= heap.heap[left])
            if right < len(heap.heap):
                self.assertTrue(heap.heap[i] >= heap.heap[right])

        extracted = []
        while len(heap) > 0:
            extracted.append(heap.extract())
        self.assertEqual(extracted, [9, 7, 6, 5, 2, 1])

    def test_heap_property_after_operations(self):
        """Тест сохранения свойства кучи после операций."""
        heap = Heap(is_min=True)

        import random
        for _ in range(100):
            heap.insert(random.randint(0, 1000))

        for i in range(len(heap.heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(heap.heap):
                self.assertTrue(heap.heap[i] <= heap.heap[left])
            if right < len(heap.heap):
                self.assertTrue(heap.heap[i] <= heap.heap[right])

        prev = None
        while len(heap) > 0:
            current = heap.extract()
            if prev is not None:
                self.assertTrue(prev <= current)
            prev = current

    def test_len_and_str(self):
        """Тест методов __len__ и __str__."""
        heap = Heap(is_min=True)
        self.assertEqual(len(heap), 0)
        self.assertEqual(str(heap), "[]")

        heap.insert(5)
        heap.insert(3)
        self.assertEqual(len(heap), 2)


if __name__ == '__main__':
    unittest.main()
