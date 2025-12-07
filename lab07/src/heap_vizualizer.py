"""Визуализация кучи в виде дерева."""
from heap import Heap


def visualize_heap(heap: Heap) -> str:
    """Возвращает строку с визуализацией кучи в виде дерева."""
    if not heap.heap:
        return "(пустая куча)"

    elements = heap.heap
    n = len(elements)

    depth = 0
    while (1 << depth) - 1 < n:
        depth += 1

    max_width = max(len(str(x)) for x in elements)

    result_lines = []
    result_lines.append(
        f"{'MIN' if heap.is_min else 'MAX'}-HEAP ({n} элементов):")
    result_lines.append("=" * 40)

    for level in range(depth):
        start = (1 << level) - 1
        end = min((1 << (level + 1)) - 1, n)

        level_count = end - start

        chars = (1 << (depth - 1)) * (max_width + 2)

        cell_width = chars // level_count if level_count > 0 else chars

        level_line = ""
        for i in range(start, end):
            element_str = str(elements[i])
            left_pad = (cell_width - len(element_str)) // 2
            right_pad = cell_width - len(element_str) - left_pad
            level_line += " " * left_pad + element_str + " " * right_pad

        result_lines.append(level_line.rstrip())

    return "\n".join(result_lines)


def print_heap_pretty(heap: Heap) -> None:
    """Печатает кучу как дерево."""
    if not heap.heap:
        print("(пустая куча)")
        return

    elements = heap.heap
    n = len(elements)

    depth = 0
    while (1 << depth) - 1 < n:
        depth += 1

    max_num_width = max(len(str(x)) for x in elements)
    fixed_width = max(2, max_num_width)

    print(f"\n{'MIN' if heap.is_min else 'MAX'}-HEAP ({n} элементов):")
    print("-" * 40)

    if n <= 31:
        for level in range(depth):
            start = (1 << level) - 1
            end = min((1 << (level + 1)) - 1, n)

            indent = " " * ((1 << (depth - level - 1)) - 1) * (fixed_width + 1)

            spacing = " " * ((1 << (depth - level)) - 1) * (fixed_width + 1)

            level_str = indent
            for i in range(start, end):
                if i > start:
                    level_str += spacing
                level_str += f"{elements[i]:>{fixed_width}}"

            print(level_str)
    else:
        for level in range(depth):
            start = (1 << level) - 1
            end = min((1 << (level + 1)) - 1, n)
            level_elements = elements[start:end]
            print(
                f"Уровень {level}: {' '.join(str(x) for x in level_elements)}")


def main():
    """Основная функция демонстрации."""
    test_cases = [
        ("MIN-HEAP из [30, 10, 50, 5, 15, 40, 60]",
         [30, 10, 50, 5, 15, 40, 60], True),

        ("MAX-HEAP из тех же чисел",
         [30, 10, 50, 5, 15, 40, 60], False),

        ("MIN-HEAP из [9, 4, 7, 1, 3, 6, 2, 8, 5]",
         [9, 4, 7, 1, 3, 6, 2, 8, 5], True),
    ]

    for name, data, is_min in test_cases:
        print(f"\n{name}:")
        heap = Heap(is_min=is_min)
        heap.build_heap(data)
        print_heap_pretty(heap)
        print(f"Массив: {heap.heap}")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ:")
    print("=" * 50)

    heap = Heap(is_min=True)
    heap.build_heap([30, 10, 50, 5, 15, 40, 60])

    print("\nНачальная куча:")
    print_heap_pretty(heap)

    print("\nИзвлекаем элементы:")
    extracted = []
    while heap.heap:
        extracted.append(heap.extract())
        if len(heap.heap) <= 7:
            print(f"\nПосле извлечения {extracted[-1]}:")
            print_heap_pretty(heap)

    print(f"\nВсе извлечённые элементы: {extracted}")


if __name__ == "__main__":
    main()
