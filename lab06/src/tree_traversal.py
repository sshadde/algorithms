from typing import List, Optional
from binary_search_tree import TreeNode


def in_order_recursive(node: Optional[TreeNode], result: List[int]) -> None:
    """Рекурсивный in-order обход (левый-корень-правый)"""
    if node:
        in_order_recursive(node.left, result)
        result.append(node.value)
        in_order_recursive(node.right, result)


def pre_order_recursive(node: Optional[TreeNode], result: List[int]) -> None:
    """Рекурсивный pre-order обход (корень-левый-правый)"""
    if node:
        result.append(node.value)
        pre_order_recursive(node.left, result)
        pre_order_recursive(node.right, result)


def post_order_recursive(node: Optional[TreeNode], result: List[int]) -> None:
    """Рекурсивный post-order обход (левый-правый-корень)"""
    if node:
        post_order_recursive(node.left, result)
        post_order_recursive(node.right, result)
        result.append(node.value)


def in_order_iterative(root: Optional[TreeNode]) -> List[int]:
    """Итеративный in-order обход с использованием стека"""
    result: List[int] = []
    stack: List[TreeNode] = []
    current: Optional[TreeNode] = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        result.append(current.value)

        current = current.right

    return result
