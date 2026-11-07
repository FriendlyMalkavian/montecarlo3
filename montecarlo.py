"""
Модуль с логикой моделирования биномиального распределения
методом Монте-Карло и построением графика.
"""

import math
from random import random
import io
import base64

import matplotlib
matplotlib.use('Agg')  # неблокирующий backend — обязателен для сервера
import matplotlib.pyplot as plt


# ---------- Логика расчётов ----------
def MonteCarloBinomial(numberOfExperiments, N_trials, p):
    experiments = []
    for _ in range(numberOfExperiments):
        successes = 0
        for _ in range(N_trials):
            if random() < p:
                successes += 1
        experiments.append(successes)

    segments = list(range(N_trials + 1))
    results = [0] * (N_trials + 1)

    for value in experiments:
        results[value] += 1

    y_values = [count / numberOfExperiments for count in results]
    return segments, y_values, experiments


def theoryBinomial(m, N, p):
    """P(X=m) = C(N,m) * p^m * (1-p)^(N-m)"""
    C = math.comb(N, m)
    return C * (p ** m) * ((1 - p) ** (N - m))


# ---------- Валидация входных данных ----------
def validate_inputs(n_str, p_str, ch_str):
    errors = []

    # n
    try:
        n = int(n_str)
        if n <= 0:
            errors.append("n должно быть натуральным числом")
    except (ValueError, TypeError):
        errors.append("Некорректное значение n")
        n = None

    # p
    try:
        p_raw = p_str.replace(',', '.')
        p = float(p_raw)
        if not (0 < p <= 1):
            errors.append("Вероятность p должна быть в диапазоне (0, 1]")
    except (ValueError, TypeError, AttributeError):
        errors.append("Некорректное значение p")
        p = None

    # ch
    try:
        ch = int(ch_str)
        if ch <= 0:
            errors.append("Число опытов должно быть натуральным")
        if ch > 1_000_000:
            errors.append("Слишком большое число опытов (>1 000 000). Уменьшите значение.")
    except (ValueError, TypeError):
        errors.append("Некорректное значение числа опытов")
        ch = None

    return n, p, ch, errors


# ---------- Построение графика в base64 ----------
def build_plot(n, p, ch):
    segments, y_values, _ = MonteCarloBinomial(ch, n, p)
    y_theory = [theoryBinomial(m, n, p) for m in segments]

    plt.figure(figsize=(10, 6))
    plt.bar(segments, y_values, width=0.6, color='skyblue',
            edgecolor='black', alpha=0.7, label='Монте-Карло')
    plt.plot(segments, y_theory, 'ro-', linewidth=2, markersize=6,
             label=f'Теория (n={n}, p={p})')
    plt.xlabel('Число успехов m')
    plt.ylabel('Относительная частота P(X = m)')
    plt.title('Биномиальное распределение: метод Монте-Карло и теория')
    plt.xticks(segments)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Сохраняем в буфер и кодируем в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # обязательно, чтобы не было утечки памяти
    buf.seek(0)
    img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return img_b64
    
    
            

 