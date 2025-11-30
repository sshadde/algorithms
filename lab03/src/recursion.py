"""Модуль с реализацией классических рекурсивных алгоритмов."""

import time
from typing import Any, Optional


def factorial(n: int) -> int:
    """
    Вычисление факториала числа n рекурсивным способом.

    Args:
        n: Целое неотрицательное число
    Returns:
        Факториал числа n
    Raises:
        ValueError: Если n < 0
    """
    if n < 0:
        raise ValueError('Факториала для отрицательных чисел не существует.')
    if n == 0:
        return 1
    return n * factorial(n - 1)
# Временная сложность: O(n)
# Глубина рекурсии: O(n)


def fibonacci(n: int, counter: Optional[list] = None) -> int:
    """
    Наивное вычисление чисел Фибоначчи с подсчётом вызовов.

    Args:
        n: Порядковый номер числа Фибоначчи
        counter: Список для подсчёта вызовов [количество_вызовов]
    Returns:
        n-е число Фибоначчи
    """
    if counter is None:
        counter = [0]

    counter[0] += 1

    if n <= 1:
        return n

    return (fibonacci(n - 1, counter) +
            fibonacci(n - 2, counter))
# Временная сложность: O(2^n)
# Глубина рекурсии: O(n)


def fast_power(a: float, n: int) -> float:
    """
    Быстрое возведение числа a в степень n через степень двойки.

    Args:
        a: Основание
        n: Показатель степени
    Returns:
        a в степени n
    """
    if n == 0:
        return 1
    if n < 0:
        return 1 / fast_power(a, -n)

    if n % 2 == 0:
        half_power = fast_power(a, n // 2)
        return half_power * half_power

    else:
        return a * fast_power(a, n - 1)
# Временная сложность: O(log n)
# Глубина рекурсии: O(log n)


def measure_execution_time(func: Any, *args: Any) -> tuple[Any, float]:
    """
    Измерение времени выполнения функции.

    Args:
        func: Функция для измерения
        *args: Аргументы функции
    Returns:
        Кортеж (результат, время выполнения в секундах)
    """
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time


if __name__ == '__main__':
    print('=== Рекурсивные алгоритмы ===')

    print(f'Факториал 5: {factorial(5)}')

    print(f'Фибоначчи(10): {fibonacci(10)}')

    print(f'2^10: {fast_power(2, 10)}')
    print(f'2^(-3): {fast_power(2, -3)}')

    print('\n=== Замер времени для Фибоначчи ===')
    for i in [5, 10, 15, 20, 25]:
        result, exec_time = measure_execution_time(fibonacci, i)
        print(f'fibonacci({i}) = {result}, время: {exec_time:.6f} сек')
