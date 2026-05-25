import math

def log_result(func):
    """Decorator to print formatted calculation results."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"x: {result[0]}\nn: {result[1]}\nF(x): {result[2]}\nMath F(x): {result[3]}\neps: {result[4]}");
        return result
    return wrapper

@log_result
def calculate_series(x, eps):
    """Calculates ln(1-x) series expansion and compares with math.log."""
    max_iterations = 500
    n = 1
    current_sum = 0.0
    term = -x

    while abs(term) > eps and n < max_iterations:
        current_sum += term
        n += 1
        term = -(x**n) / n
    
    math_f_x = math.log(1-x)
    return [x, n, current_sum, math_f_x, eps]

def get_user_input():
    """Prompts user for x and eps with basic error handling."""
    while True:
        try:
            x = float(input("Enter x (|x| < 1): "))
            eps = float(input("Enter precision: "))
            return x, eps
        except ValueError:
            print("Error: enter valid numeric values.")
