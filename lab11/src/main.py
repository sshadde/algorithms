"""Основной файл для демонстрации работы всех алгоритмов."""

from string_matching import rabin_karp_search
from z_function import z_function, z_search, is_cyclic_shift
from kmp_search import kmp_search
from prefix_function import prefix_function, find_string_period
import time
import random
import matplotlib.pyplot as plt


def demonstrate_algorithms() -> None:
    """Демонстрация работы всех реализованных алгоритмов."""
    text = "ababcababcababc"
    pattern = "ababc"

    print(f"\nText: '{text}'")
    print(f"Pattern: '{pattern}'")
    print("-" * 60)

    print("\n1. PREFIX FUNCTION:")
    prefix = prefix_function(pattern)
    print(f"   Prefix function for pattern: {prefix}")

    period = find_string_period(text)
    print(f"   Period of string '{text}': {period}")

    print("\n2. KNUTH-MORRIS-PRATT ALGORITHM (KMP):")
    indices_kmp = kmp_search(text, pattern)
    print(f"   Match indices (KMP): {indices_kmp}")

    print("\n3. Z-FUNCTION:")
    z = z_function(pattern)
    print(f"   Z-function for pattern: {z}")

    indices_z = z_search(text, pattern)
    print(f"   Match indices (Z-search): {indices_z}")

    print("\n4. RABIN-KARP ALGORITHM:")
    indices_rk = rabin_karp_search(text, pattern)
    print(f"   Match indices (Rabin-Karp): {indices_rk}")

    print("\n5. CYCLIC SHIFT CHECK:")
    s1 = "abcdef"
    s2 = "defabc"
    s3 = "fedcba"

    result1 = is_cyclic_shift(s1, s2)
    result2 = is_cyclic_shift(s1, s3)

    print(f"   '{s2}' is cyclic shift of '{s1}': {result1}")
    print(f"   '{s3}' is cyclic shift of '{s1}': {result2}")


def compare_performance() -> None:
    """Сравнение времени выполнения алгоритмов с построением графика."""
    def generate_random_string(length: int) -> str:
        letters = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join(random.choice(letters) for _ in range(length))

    def measure_time(func, *args) -> float:
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        return end - start

    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    text_lengths = [1000, 2000, 5000, 10000]
    pattern_length = 100
    results_kmp = []
    results_z = []
    results_rk = []

    for text_length in text_lengths:
        text = generate_random_string(text_length)
        pattern = generate_random_string(pattern_length)

        time_kmp = measure_time(kmp_search, text, pattern)
        time_z = measure_time(z_search, text, pattern)
        time_rk = measure_time(rabin_karp_search, text, pattern)

        results_kmp.append(time_kmp)
        results_z.append(time_z)
        results_rk.append(time_rk)

        print(f"\nText length: {text_length}")
        print(f"  KMP:        {time_kmp:.6f} sec")
        print(f"  Z-search:   {time_z:.6f} sec")
        print(f"  Rabin-Karp: {time_rk:.6f} sec")

    plt.figure(figsize=(10, 6))
    plt.plot(text_lengths, results_kmp, marker='o', label='KMP', linewidth=2)
    plt.plot(text_lengths, results_z, marker='s',
             label='Z-search', linewidth=2)
    plt.plot(text_lengths, results_rk, marker='^',
             label='Rabin-Karp', linewidth=2)

    plt.title('Сравнение производительности алгоритмов поиска подстрок',
              fontsize=14)
    plt.xlabel('Длина текста (символы)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()

    plt.savefig('report/performance_comparison.png', dpi=300)
    print("\nГрафик сохранен в 'report/performance_comparison.png'")


def test_different_string_types() -> None:
    """Тестирование на строках разных типов."""
    print("\n" + "=" * 60)
    print("TESTING ON DIFFERENT STRING TYPES")
    print("=" * 60)

    print("\n1. RANDOM STRINGS:")
    random_text = "xkjshdfkjhsdf"
    random_pattern = "kjh"
    print(f"   Text: '{random_text}', Pattern: '{random_pattern}'")
    print(f"   KMP matches: {kmp_search(random_text, random_pattern)}")

    print("\n2. PERIODIC STRINGS:")
    periodic_text = "abcabcabcabc"
    periodic_pattern = "abc"
    print(f"   Text: '{periodic_text}', Pattern: '{periodic_pattern}'")
    print(f"   KMP matches: {kmp_search(periodic_text, periodic_pattern)}")
    print(f"   Period: {find_string_period(periodic_text)}")

    print("\n3. STRINGS WITH REPETITIONS:")
    repeat_text = "aaaaaaa"
    repeat_pattern = "aa"
    print(f"   Text: '{repeat_text}', Pattern: '{repeat_pattern}'")
    print(f"   KMP matches: {kmp_search(repeat_text, repeat_pattern)}")


if __name__ == "__main__":
    demonstrate_algorithms()
    compare_performance()
    test_different_string_types()
