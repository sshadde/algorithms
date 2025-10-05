from __future__ import annotations
from collections import deque
import statistics
from typing import Deque, Dict, List, Sequence, Tuple, TypeVar, TypedDict

T = TypeVar('T')


def is_brackets_balanced(s: str) -> bool:
    """Проверить, сбалансированы ли скобки в строке s.
    Поддерживаются пары: (), [], {}.
    Сложность: O(n).
    """
    pairs: Dict[str, str] = {')': '(', ']': '[', '}': '{'}
    stack: List[str] = []

    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()

    return len(stack) == 0


class ProcessedJob(TypedDict):
    """Тип для описания одного обработанного задания печати."""
    id: str
    arrival: float
    start: float
    finish: float
    pages: int
    wait: float
    turnaround: float


def print_sim(
    jobs: List[Tuple[str, float, int]],
    pages_per_min: int = 10
) -> Tuple[List[ProcessedJob], Dict[str, float]]:
    """Симуляция печати (FIFO), использует deque.
    Атрибуты:
        jobs: список кортежей (job_id, arrival_time_min, pages).
        pages_per_min: скорость печати (страниц в минуту).
    Возвращаемые значения:
        processed: список словарей ProcessedJob с временами.
        stats: словарь со статистикой (processed_count, avg_wait,
            median_wait, avg_turnaround).
    """
    q: Deque[Tuple[str, float, int]] = deque(sorted(jobs, key=lambda x: x[1]))
    processed: List[ProcessedJob] = []
    clock: float = 0.0

    while q:
        job_id, arrival, pages = q.popleft()
        start: float = max(clock, arrival)
        duration: float = pages / pages_per_min
        finish: float = start + duration
        wait: float = start - arrival
        turnaround: float = finish - arrival

        processed.append(
            {
                'id': job_id,
                'arrival': arrival,
                'start': start,
                'finish': finish,
                'pages': pages,
                'wait': wait,
                'turnaround': turnaround,
            }
        )

        clock = finish

    waits: List[float] = [p['wait'] for p in processed]
    turns: List[float] = [p['turnaround'] for p in processed]
    stats: Dict[str, float] = {
        'processed_count': float(len(processed)),
        'avg_wait': statistics.mean(waits) if waits else 0.0,
        'median_wait': statistics.median(waits) if waits else 0.0,
        'avg_turnaround': statistics.mean(turns) if turns else 0.0,
    }
    return processed, stats


def is_palindrome(seq: Sequence[T]) -> bool:
    """Проверка, является ли последовательность палиндромом (O(n))."""
    dq: Deque[T] = deque(seq)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


if __name__ == '__main__':
    print('Задание 1:')
    print(is_brackets_balanced('{[()]}'))   # True
    print(is_brackets_balanced('{[(])}'))   # False

    print('\nЗадание 2:')
    jobs_example: List[Tuple[str, float, int]] = [
        ('A', 0.0, 4),   # id, arrival(min), pages
        ('B', 0.5, 2),
        ('C', 1.0, 10),
        ('D', 1.0, 1),
    ]
    proc, st = print_sim(jobs_example, pages_per_min=5)
    print('stats:', st)
    for p in proc:
        print(p)

    print('\nЗадание 3:')
    print(is_palindrome('radar'))            # True
    print(is_palindrome([1, 6, 3, 2, 5]))    # False
    print(is_palindrome([7, 5, 4, 3, 4, 5, 7]))  # True
