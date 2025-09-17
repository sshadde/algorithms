'''
sum_analysis.py
Чтение двух чисел из stdin или файла, вывод их суммы.
'''

import sys  # O(1). Импорт для работы со стандартным вводом/выводом.
from typing import Optional  # O(1). Для аннотаций типов.


def calculate_sum_from_file(path: str) -> Optional[int]:
    '''
    Открывает файл, ожидает ровно два числа (на одной или на двух строках),
    преобразует их в int и возвращает их сумму.
    '''
    try:
        with open(path, 'r', encoding='utf-8') as fh:  # O(1). Открытие файла.
            content = fh.read()  # O(F). Чтение файла, F - размер в символах.
    except OSError as exc:
        print(f'Не удалось открыть файл: {exc}.')  # O(1).
        return None  # O(1).

    # Разбиваем по любым пробельным символам (новая строка, пробелы и т.п.).
    tokens = content.split()  # O(T). T - число токенов.
    if len(tokens) != 2:  # O(1).
        print('Ошибка: файл должен содержать ровно два числа.')  # O(1).
        return None  # O(1).

    # Попытка преобразовать оба токена в целые числа.
    try:
        a = int(tokens[0])  # O(1).
        b = int(tokens[1])  # O(1).
    except ValueError:
        print('Ошибка: токен файла не является целым числом.')  # O(1).
        return None  # O(1).

    result = a + b  # O(1). Сложение двух чисел.
    print(result)  # O(1). Печать результата.
    # Общая сложность функции: O(F).
    return result  # O(1).


def calculate_sum_from_stdin() -> None:
    '''
    Считывает две строки из stdin, пытается преобразовать их в целые
    и печатает сумму. При ошибке выводит сообщение.
    '''
    line1 = sys.stdin.readline()  # O(1). Чтение первой строки.
    if not line1:  # O(1).
        print('Ошибка: ожидалась первая строка с целым числом.')  # O(1).
        return  # O(1).
    try:
        a = int(line1.strip())  # O(1). Преобразование в int.
    except ValueError:
        print('Ошибка: первая строка не целое число.')  # O(1).
        return  # O(1).

    line2 = sys.stdin.readline()  # O(1). Чтение второй строки.
    if not line2:  # O(1).
        print('Ошибка: ожидалась вторая строка с целым числом.')  # O(1).
        return  # O(1).
    try:
        b = int(line2.strip())  # O(1). Преобразование в int.
    except ValueError:
        print('Ошибка: вторая строка не целое число.')  # O(1).
        return  # O(1).

    result = a + b  # O(1). Сложение двух чисел.
    print(result)  # O(1). Вывод результата.
    # Общая сложность функции: O(1).


def main() -> None:
    '''
    Обработчик аргументов командной строки. Если указан флаг --sum-file,
    вызывается чтение из файла, иначе используется чтение из stdin.
    '''
    # Обработка аргументов.
    if len(sys.argv) >= 3 and sys.argv[1] == '--sum-file':  # O(1).
        path = sys.argv[2]  # O(1).
        calculate_sum_from_file(path)  # O(F) - зависит от размера файла.
    elif len(sys.argv) == 1:  # O(1).
        # Запуск без аргументов предполагает чтение из stdin.
        calculate_sum_from_stdin()  # O(1).
    else:
        print('Использование:')  # O(1).
        print('  python sum_analysis.py')  # O(1).
        print('  python sum_analysis.py --sum-file path_to_file')  # O(1).


if __name__ == '__main__':  # O(1).
    main()  # O(1).
