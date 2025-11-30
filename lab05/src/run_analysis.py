"""
Скрипт для запуска полного анализа производительности хеш-таблиц.
"""

from performance_analysis import PerformanceAnalyzer


def main():
    analyzer = PerformanceAnalyzer()

    analyzer.run_comparative_analysis()

    print("\nПостроение графиков...")
    analyzer.plot_performance_comparison()
    analyzer.plot_collision_histograms()

    print("\nАнализ завершен! Результаты сохранены в файлы:")
    print("- performance_comparison.png")
    print("- collision_histograms.png")


if __name__ == "__main__":
    main()
