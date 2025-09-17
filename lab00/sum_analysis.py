'''
sum_analysis.py
Чтение двух чисел из stdin или файла, вывод их суммы.
'''

import sys  # O(1). Импорт для работы со stdin/stdout.
import timeit  # O(1). Модуль для точных замеров времени.
import random  # O(1). Для генерации тестовых массивов.
import statistics  # O(1). Для среднего и std.
import csv  # O(1). Для записи CSV.
import os  # O(1). Для работы с файловой системой.
import json  # O(1). Для сохранения sysinfo.
import platform  # O(1). Для получения инфы о системе.
from typing import Optional, List, Iterable, Dict  # O(1). Аннотации типов.


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


def sum_array(arr: Iterable[int]) -> int:
    '''
    Возвращает сумму всех элементов коллекции.
    Теоретическая сложность: O(N).
    '''
    total = 0  # O(1). Инициализация.
    for x in arr:  # O(N). Проход по всем элементам.
        total += x  # O(1). Сложение и присваивание.
    return total  # O(1). Возврат результата.
    # Общая сложность функции: O(N).


def measure_time(func, data, repeats: int = 3) -> float:
    '''
    Измеряет среднее время выполнения func(data) в миллисекундах.
    Используется timeit.timeit для более стабильных измерений.
    '''
    total = timeit.timeit(lambda: func(data), number=repeats)  # O(rep*cost).
    avg_ms = (total / repeats) * 1000.0  # O(1). Конвертация в миллисекунды.
    return avg_ms  # O(1).
    # Общая сложность функции: O(repeats*cost).


def run_measurements(out_dir: str,
                     sizes: List[int],
                     repeats_policy: Optional[Dict[int, int]] = None) -> None:
    '''
    Проводит замеры sum_array для каждого N в sizes.
    Сохраняет CSV, отчёт (Markdown) и пытается построить PNG-график.
    '''
    if repeats_policy is None:
        repeats_policy = {}

    os.makedirs(out_dir, exist_ok=True)  # O(1). Создание папки результата.
    results = []  # O(1). Сбор результатов.

    for n in sizes:  # O(len(sizes)).
        repeats = repeats_policy.get(n, 5)  # O(1).
        samples: List[float] = []  # O(1).
        for _ in range(repeats):  # O(repeats).
            data = [random.randint(0, 1000) for _ in range(n)]  # O(n).
            t = timeit.timeit(lambda: sum_array(data), number=1)  # O(cost).
            samples.append(t * 1000.0)  # O(1).
        avg_ms = statistics.mean(samples)  # O(repeats).
        if len(samples) > 1:
            std_ms = statistics.stdev(samples)  # O(reps).
        else:
            std_ms = 0.0
        results.append({'N': n, 'avg_ms': avg_ms, 'std_ms': std_ms,
                        'repeats': repeats})  # O(1).
        print(f'N={n:7d}  avg={avg_ms:9.4f} ms  std={std_ms:9.4f} ms  '
              f'repeats={repeats}')

    # Сохраняем CSV.
    csv_path = os.path.join(out_dir, 'time_measurements.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['N', 'avg_ms', 'std_ms',
                                                'repeats'])
        writer.writeheader()
        writer.writerows(results)

    # Пытаемся построить график, если доступен matplotlib.
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        print('matplotlib не установлен. PNG график не будет создан.')
        png_path = None
    else:
        Ns = [r['N'] for r in results]
        avgs = [r['avg_ms'] for r in results]
        plt.figure(figsize=(8, 5))
        plt.plot(Ns, avgs, marker='o', linestyle='-')
        plt.xlabel('Размер массива (N)')
        plt.ylabel('Время выполнения (мс)')
        plt.title('Зависимость времени выполнения от N. O(N) ожидается.')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        png_path = os.path.join(out_dir, 'time_complexity_plot.png')
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        plt.close()

    # Сохраняем системную информацию.
    sysinfo = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'processor': platform.processor(),
        'cpu_count': os.cpu_count(),
    }
    with open(os.path.join(out_dir, 'sysinfo.json'),
              'w', encoding='utf-8') as fh:
        json.dump(sysinfo, fh, ensure_ascii=False, indent=2)

    # Формируем Markdown-отчёт.
    report_path = os.path.join(out_dir, 'report.md')
    with open(report_path, 'w', encoding='utf-8') as fh:
        fh.write('# Отчёт по лабораторной работе 00\n\n')
        fh.write('**Краткое содержание:** замеры sum_array, CSV и график.\n\n')
        fh.write('## Системная информация\n\n')
        fh.write(f"- Платформа: {sysinfo['platform']}\n")
        fh.write(f"- Python: {sysinfo['python_version']}\n")
        fh.write(f"- Процессор: {sysinfo['processor']}\n")
        fh.write(f"- Число логических ядер: {sysinfo['cpu_count']}\n\n")
        fh.write('## Результаты замеров\n\n')
        fh.write('Таблица результатов записана в time_measurements.csv.\n\n')
        if png_path:
            fh.write('![График зависимости времени от N]'
                     f'({os.path.basename(png_path)})\n\n')
        for r in results:
            fh.write(f"- N={r['N']}: avg={r['avg_ms']:.6f} ms, "
                     f"std={r['std_ms']:.6f} ms, repeats={r['repeats']}\n")
    # Общая сложность: O(sum_{n in sizes} (repeats[n] * n)).


def main() -> None:
    '''
    Обработчик аргументов. Поддерживает:
    --sum-file <path>    : читать из файла.
    --run-all            : провести замеры и сохранить результаты.
    --out-dir <path>     : каталог для результатов.
    --sizes <csv>        : перечень размеров N через запятую.
    '''
    # Простая обработка командной строки.
    if len(sys.argv) >= 3 and sys.argv[1] == '--sum-file':  # O(1).
        path = sys.argv[2]  # O(1).
        calculate_sum_from_file(path)  # O(F).
        return  # O(1).

    # Флаг --run-all для проведения замеров.
    if len(sys.argv) >= 2 and sys.argv[1] == '--run-all':  # O(1).
        # Значения по умолчанию.
        out_dir = 'lab00_output'  # O(1).
        sizes = [1000, 5000, 10000, 50000, 100000]  # O(1).

        # Если передан --out-dir.
        if '--out-dir' in sys.argv:  # O(1).
            try:
                idx = sys.argv.index('--out-dir')  # O(n_args).
                out_dir = sys.argv[idx + 1]  # O(1).
            except (ValueError, IndexError):
                print('Ошибка: укажите путь после --out-dir.')  # O(1).
                return  # O(1).

        # Если передан --sizes в виде CSV, например: --sizes 1000,5000.
        if '--sizes' in sys.argv:  # O(1).
            try:
                idx = sys.argv.index('--sizes')  # O(n_args).
                raw = sys.argv[idx + 1]  # O(1).
                sizes = [int(x) for x in raw.split(',') if x.strip()]  # O(k).
            except Exception:
                print('Ошибка: неверный формат для --sizes.')  # O(1).
                return  # O(1).

        # Политика повторов: меньше повторов для больших N.
        repeats_policy: Dict[int, int] = {}  # O(1).
        for n in sizes:
            if n <= 10000:
                repeats_policy[n] = 10
            elif n <= 50000:
                repeats_policy[n] = 5
            elif n <= 200000:
                repeats_policy[n] = 3
            else:
                repeats_policy[n] = 2

        print('Запуск замеров. Результаты будут в:', out_dir)  # O(1).
        run_measurements(out_dir, sizes, repeats_policy)  # O(total_work).
        return  # O(1).

    # По умолчанию читаем из stdin.
    if len(sys.argv) == 1:  # O(1).
        calculate_sum_from_stdin()  # O(1).
    else:
        print('Использование:')  # O(1).
        print('  python sum_analysis.py')  # O(1).
        print('  python sum_analysis.py --sum-file path_to_file')  # O(1).
        print('  python sum_analysis.py --run-all [--out-dir dir]')  # O(1).
        print('  python sum_analysis.py --run-all --sizes 1000,5000')  # O(1).


if __name__ == '__main__':  # O(1).
    main()  # O(1).
