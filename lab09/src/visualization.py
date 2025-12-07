"""Визуализация заполнения таблицы ДП для рюкзака"""


def visualize_knapsack_table(weights, values, capacity):
    """Визуализация таблицы ДП для задачи о рюкзаке"""
    n = len(weights)

    print("=" * 60)
    print("ВИЗУАЛИЗАЦИЯ ЗАПОЛНЕНИЯ ТАБЛИЦЫ ДП ДЛЯ РЮКЗАКА")
    print("=" * 60)
    print(f"Предметы: {list(zip(weights, values))}")
    print(f"Вместимость: {capacity}")
    print()

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    print("Начальная таблица (все нули):")
    print_table(dp, weights)
    print()

    for i in range(1, n + 1):
        print(
            f"\n--- Шаг {i}: рассматриваем предмет {i-1} "
            f"(вес={weights[i-1]}, стоимость={values[i-1]}) ---")

        for w in range(1, capacity + 1):
            print(f"\n  Для вместимости w={w}:")

            if weights[i-1] <= w:
                not_take = dp[i-1][w]
                take = dp[i-1][w - weights[i-1]] + values[i-1]

                print(
                    f"    Вариант 1: не брать предмет → "
                    f"dp[{i-1}][{w}] = {not_take}")
                print(
                    f"    Вариант 2: брать предмет → dp[{i-1}]"
                    f"[{w}-{weights[i-1]}] + {values[i-1]} = "
                    f"dp[{i-1}][{w-weights[i-1]}] + {values[i-1]} = "
                    f"{dp[i-1][w - weights[i-1]]} + {values[i-1]} = {take}")

                if take > not_take:
                    dp[i][w] = take
                    print(f"    Выбираем вариант 2 (брать): {take}")
                else:
                    dp[i][w] = not_take
                    print(f"    Выбираем вариант 1 (не брать): {not_take}")
            else:
                dp[i][w] = dp[i-1][w]
                print(f"    Предмет не помещается ({weights[i-1]} > {w})")
                print(f"    Берем dp[{i-1}][{w}] = {dp[i-1][w]}")

        print(f"\nТаблица после шага {i}:")
        print_table(dp, weights)

    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ТАБЛИЦА:")
    print_table(dp, weights)

    print("\n" + "=" * 60)
    print("ВОССТАНОВЛЕНИЕ РЕШЕНИЯ:")

    w = capacity
    selected_items = []

    print("Начинаем с правого нижнего угла dp[n][W]:")

    for i in range(n, 0, -1):
        print(f"\n  Проверяем предмет {i-1}:")
        print(f"    dp[{i}][{w}] = {dp[i][w]}")
        print(f"    dp[{i-1}][{w}] = {dp[i-1][w]}")

        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
            print(f"    → Предмет {i-1} ВЫБРАН!")
            print(f"    Новая вместимость: {w}")
        else:
            print(f"    → Предмет {i-1} НЕ выбран")

    selected_items.reverse()

    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ:")
    print(f"Максимальная стоимость: {dp[n][capacity]}")
    print(f"Выбранные предметы: {selected_items}")

    total_weight = 0
    total_value = 0
    for idx in selected_items:
        total_weight += weights[idx]
        total_value += values[idx]
        print(f"  Предмет {idx}: вес {weights[idx]}, стоимость {values[idx]}")

    print(f"Общий вес: {total_weight}/{capacity}")
    print(f"Общая стоимость: {total_value}")

    return dp[n][capacity], selected_items


def print_table(dp, weights):
    """Вывод таблицы"""
    n = len(weights)
    capacity = len(dp[0]) - 1

    print("  w |", end="")
    for w in range(capacity + 1):
        print(f" {w:3}", end="")
    print()
    print(" ---+" + "-" * (4 * (capacity + 1)))

    for i in range(n + 1):
        if i == 0:
            print(" i=0|", end="")
        else:
            print(f" i={i}|", end="")

        for w in range(capacity + 1):
            print(f" {dp[i][w]:3}", end="")
        print()


if __name__ == "__main__":
    """Запуск визуализации."""
    weights = [2, 3, 4]
    values = [3, 4, 5]
    capacity = 5

    visualize_knapsack_table(weights, values, capacity)
