"""Тестирование бинарного дерева поиска."""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from binary_search_tree import BinarySearchTree  # type: ignore # noqa: E402


class TestBinarySearchTree(unittest.TestCase):
    """Класс unit-тест."""

    def setUp(self):
        """Инициализация бинарного дерева."""
        self.bst = BinarySearchTree()

    def test_insert_and_search(self):
        """Тестирование вставки и поиска."""
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)

        self.assertTrue(self.bst.search(5))
        self.assertTrue(self.bst.search(3))
        self.assertTrue(self.bst.search(7))
        self.assertFalse(self.bst.search(10))

    def test_delete(self):
        """Тестирование удаления узла."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.bst.insert(value)

        self.bst.delete(3)
        self.assertFalse(self.bst.search(3))
        self.assertTrue(self.bst.search(2))
        self.assertTrue(self.bst.search(4))

    def test_is_valid_bst(self):
        """Проверка на BST."""
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)
        self.assertTrue(self.bst.is_valid_bst())

    def test_find_min_max(self):
        """Поиск максимума и минимума."""
        values = [5, 3, 7, 1, 9]
        for value in values:
            self.bst.insert(value)

        self.assertEqual(self.bst.find_min(self.bst.root).value, 1)
        self.assertEqual(self.bst.find_max(self.bst.root).value, 9)


if __name__ == '__main__':
    unittest.main()
