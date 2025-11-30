from typing import Optional


class TreeNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinarySearchTree:
    """Бинарное дерево поиска."""

    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    def insert(self, value: int) -> None:
        """
        Вставка элемента в дерево.

        Сложность:
          - Средний случай: O(log n)
          - Худший случай: O(n) - вырожденное дерево
        """
        new_node = TreeNode(value)

        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while current:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                else:
                    current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = new_node
                    return
                else:
                    current = current.right
            else:
                return

    def search(self, value: int) -> bool:
        """
        Поиск элемента в дереве.

        Сложность:
          - Средний случай: O(log n)
          - Худший случай: O(n)
        """
        current = self.root
        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, value: int) -> None:
        """
        Удаление элемента из дерева.

        Сложность:
          - Средний случай: O(log n)
          - Худший случай: O(n)
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node: Optional[TreeNode],
                          value: int) -> Optional[TreeNode]:
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_node = self.find_min(node.right)
            if min_node is not None:
                node.value = min_node.value
            node.right = self._delete_recursive(node.right,
                                                min_node.value
                                                if min_node else value)

        return node

    def find_min(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Поиск минимального элемента в поддереве.

        Сложность:
          - Средний случай: O(log n)
          - Худший случай: O(n)
        """
        if node is None:
            return None
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_max(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Поиск максимального элемента в поддереве.

        Сложность:
          - Средний случай: O(log n)
          - Худший случай: O(n)
        """
        if node is None:
            return None
        current = node
        while current.right is not None:
            current = current.right
        return current

    def height(self, node: Optional[TreeNode]) -> int:
        """Вычисление высоты дерева/поддерева"""
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def is_valid_bst(self) -> bool:
        """Проверка, является ли дерево корректным BST"""
        return self._is_valid_recursive(self.root, float('-inf'), float('inf'))

    def _is_valid_recursive(self, node: Optional[TreeNode],
                            min_val: float, max_val: float) -> bool:
        if node is None:
            return True

        if node.value <= min_val or node.value >= max_val:
            return False

        left_valid = self._is_valid_recursive(node.left, min_val, node.value)
        right_valid = self._is_valid_recursive(node.right, node.value, max_val)

        return left_valid and right_valid

    def visualize_tree(self, node: Optional[TreeNode], level: int = 0,
                       prefix: str = "Root: ") -> str:
        """Текстовая визуализация структуры дерева"""
        if node is None:
            return ""

        result = " " * (level * 4) + prefix + str(node.value) + "\n"

        if node.left is not None or node.right is not None:
            if node.left:
                result += self.visualize_tree(node.left, level + 1, "L--- ")
            else:
                result += " " * ((level + 1) * 4) + "L--- None\n"

            if node.right:
                result += self.visualize_tree(node.right, level + 1, "R--- ")
            else:
                result += " " * ((level + 1) * 4) + "R--- None\n"

        return result
