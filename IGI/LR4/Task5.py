import numpy as np

def swap_column_maxima(matrix):    
    idx_first = np.argmax(matrix[:, 0])
    idx_last = np.argmax(matrix[:, -1])
    
    matrix[idx_first, 0], matrix[idx_last, -1] = matrix[idx_last, -1], matrix[idx_first, 0]

def get_columns_correlation(matrix):
    col_first = matrix[:, 0]
    col_last = matrix[:, -1]
    
    corr_matrix = np.corrcoef(col_first, col_last)
    correlation = corr_matrix[0, 1]
    
    return np.round(correlation, 2)

def task_5(n, m):
    data = np.random.randint(0, 100, (n, m))
    print("Matrix:\n", data)

    swap_column_maxima(data)
    print("\nMatrix after the swap:\n", data)

    corr_value = get_columns_correlation(data)
    print(f"\nCorrelation coefficient: {corr_value}")

if __name__ == "__main__":
    task_5(4,6)