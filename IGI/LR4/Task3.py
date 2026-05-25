import math
import matplotlib.pyplot as plt
import os

class SequenceCalculator:
    def __init__(self, max_iter, eps):
        self.max_iter = max_iter
        self.eps = eps

    def calculate_taylor(self, x):
        n = 1
        current_sum = 0.0
        term = -x

        while abs(term) > self.eps and n < self.max_iter:
            current_sum += term
            n += 1
            term = -(x**n) / n
        return current_sum
    
class SequenceAnalyzer:
    def get_taylor_sequence(x, n_terms):
        return [-(x**n) / n for n in range(1, n_terms + 1)]

    def calculate_mean(sequence):
        return sum(sequence) / len(sequence) if sequence else 0

    def calculate_median(sequence):
        n = len(sequence)
        if n == 0:
            return 0
        sorted_seq = sorted(sequence)
        mid = n // 2
        if n % 2 != 0:
            return sorted_seq[mid]
        return (sorted_seq[mid - 1] + sorted_seq[mid]) / 2

    def calculate_mode(sequence):
        if not sequence:
            return None
        counts = {}
        for x in sequence:
            counts[x] = counts.get(x, 0) + 1
        max_freq = max(counts.values())

        if max_freq == 1:
            return None
        for k, v in counts.items():
            if v == max_freq:
                return k

    def calculate_variance(sequence, mean):
        if not sequence:
            return 0
        return sum((x - mean) ** 2 for x in sequence) / len(sequence)

    def calculate_std_dev(variance):
        return math.sqrt(variance)
    
def task_3(x_to_analyze, n_to_analyze, out_name):
    seq_calc = SequenceCalculator(500, 0.001)
    seq_to_analyze = SequenceAnalyzer.get_taylor_sequence(x_to_analyze, n_to_analyze)

    mean = SequenceAnalyzer.calculate_mean(seq_to_analyze)
    print(f"Arithmetic mean: {round(mean, 3)}")
    print(f"Median: {round(SequenceAnalyzer.calculate_median(seq_to_analyze), 3)}")
    print(f"Mode: {SequenceAnalyzer.calculate_mode(seq_to_analyze)}")
    variance = SequenceAnalyzer.calculate_variance(seq_to_analyze, mean)
    print(f"Variance: {round(variance, 3)}")
    print(f"Standart deviation: {round(SequenceAnalyzer.calculate_std_dev(variance), 3)}")

    x_values = [i/100 for i in range(-90, 91)]

    y_taylor = [seq_calc.calculate_taylor(x) for x in x_values]
    y_math = [math.log(1 - x) for x in x_values]

    plt.figure(figsize=(10, 10))

    plt.plot(x_values, y_math, label=f'math.log(1-x)', color='blue', linewidth=2)
    plt.plot(x_values, y_taylor, label=f'Taylor Series', color='red', linestyle='--')

    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)

    plt.title(f'Comparison of math ln(1-x) and taylor series with eps {0.001}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()

    target_x = x_to_analyze
    target_y = math.log(1-target_x)

    plt.annotate('Analyzing point', 
                xy=(target_x, target_y), 
                xytext=(0.6, -0.5),
                arrowprops=dict(facecolor='black', shrink=0.05))

    folder, filename = os.path.split(out_name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    full_path = os.path.join(folder, filename)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    task_3(0.17, 6, "T3\\graph.png")