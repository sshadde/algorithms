from binary_search_tree import BinarySearchTree
from tree_traversal import (
    in_order_recursive,
    pre_order_recursive,
    post_order_recursive,
    in_order_iterative
)


def main():
    print("=== Демонстрация бинарного дерева поиска ===\n")

    bst = BinarySearchTree()
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    print("Вставляем значения:", values)
    for value in values:
        bst.insert(value)

    print("\nСтруктура дерева:")
    print(bst.visualize_tree(bst.root))

    print("In-order обход (рекурсивный):")
    result = []
    in_order_recursive(bst.root, result)
    print(result)

    print("\nPre-order обход:")
    result = []
    pre_order_recursive(bst.root, result)
    print(result)

    print("\nPost-order обход:")
    result = []
    post_order_recursive(bst.root, result)
    print(result)

    print("\nIn-order обход (итеративный):")
    print(in_order_iterative(bst.root))

    print(f"\nВысота дерева: {bst.height(bst.root)}")
    min_node = bst.find_min(bst.root)
    max_node = bst.find_max(bst.root)
    print(f"Минимальное значение: {min_node.value if min_node else 'N/A'}")
    print(f"Максимальное значение: {max_node.value if max_node else 'N/A'}")
    print(f"Является корректным BST: {bst.is_valid_bst()}")


if __name__ == "__main__":
    main()
