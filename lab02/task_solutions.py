from __future__ import annotations
from collections import deque
from typing import Deque, Dict, List, Sequence, TypeVar

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


def is_palindrome(seq: Sequence[T]) -> bool:
    """Проверка, является ли последовательность палиндромом (O(n))."""
    dq: Deque[T] = deque(seq)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True
