"""Unit-тесты для класса PriorityQueue."""
import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from priority_queue import PriorityQueue  # type: ignore  # noqa: E402


class TestPriorityQueue(unittest.TestCase):
    """Тестирование приоритетной очереди."""

    def test_min_priority_queue(self):
        """Тест min-heap приоритетной очереди (меньший приоритет = выше)."""
        pq = PriorityQueue(is_min=True)

        pq.enqueue("задача 1", 3)
        pq.enqueue("задача 2", 1)
        pq.enqueue("задача 3", 2)

        self.assertEqual(pq.dequeue(), (1, "задача 2"))
        self.assertEqual(pq.dequeue(), (2, "задача 3"))
        self.assertEqual(pq.dequeue(), (3, "задача 1"))
        with self.assertRaises(IndexError):
            pq.dequeue()

    def test_max_priority_queue(self):
        """Тест max-heap приоритетной очереди (больший приоритет = выше)."""
        pq = PriorityQueue(is_min=False)

        pq.enqueue("задача 1", 3)
        pq.enqueue("задача 2", 1)
        pq.enqueue("задача 3", 2)

        self.assertEqual(pq.dequeue(), (3, "задача 1"))
        self.assertEqual(pq.dequeue(), (2, "задача 3"))
        self.assertEqual(pq.dequeue(), (1, "задача 2"))
        with self.assertRaises(IndexError):
            pq.dequeue()

    def test_same_priority_fifo(self):
        """Тест извлечения элементов с одинаковым приоритетом."""
        pq = PriorityQueue(is_min=True)

        pq.enqueue("задача A", 1)
        pq.enqueue("задача B", 1)
        pq.enqueue("задача C", 1)
        pq.enqueue("задача D", 2)

        self.assertEqual(pq.dequeue(), (1, "задача A"))
        self.assertEqual(pq.dequeue(), (1, "задача B"))
        self.assertEqual(pq.dequeue(), (1, "задача C"))
        self.assertEqual(pq.dequeue(), (2, "задача D"))

    def test_peek(self):
        """Тест просмотра без извлечения."""
        pq = PriorityQueue(is_min=True)

        self.assertIsNone(pq.peek())

        pq.enqueue("задача 1", 5)
        pq.enqueue("задача 2", 1)

        self.assertEqual(pq.peek(), (1, "задача 2"))
        self.assertEqual(pq.peek(), (1, "задача 2"))

        pq.dequeue()
        self.assertEqual(pq.peek(), (5, "задача 1"))

    def test_len_and_is_empty(self):
        """Тест методов __len__ и is_empty."""
        pq = PriorityQueue(is_min=True)

        self.assertTrue(pq.is_empty())
        self.assertEqual(len(pq), 0)

        pq.enqueue("задача 1", 1)
        pq.enqueue("задача 2", 2)

        self.assertFalse(pq.is_empty())
        self.assertEqual(len(pq), 2)

        pq.dequeue()
        self.assertEqual(len(pq), 1)

        pq.dequeue()
        self.assertTrue(pq.is_empty())
        self.assertEqual(len(pq), 0)

    def test_mixed_operations(self):
        """Тест смешанных операций."""
        pq = PriorityQueue(is_min=True)

        pq.enqueue("низкий", 10)
        pq.enqueue("высокий", 1)
        pq.enqueue("средний", 5)

        self.assertEqual(pq.dequeue(), (1, "высокий"))

        pq.enqueue("очень высокий", 0)

        self.assertEqual(pq.peek(), (0, "очень высокий"))
        self.assertEqual(pq.dequeue(), (0, "очень высокий"))

        self.assertEqual(pq.dequeue(), (5, "средний"))
        self.assertEqual(pq.dequeue(), (10, "низкий"))


if __name__ == '__main__':
    unittest.main()
