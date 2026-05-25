def product_of_negatives(data):
    """Calculates the product of all negative numbers in the list."""
    result = 1
    has_negative = False
    
    for x in data:
        if x < 0:
            result *= x
            has_negative = True
            
    if has_negative:
        return result
    else:
        return 0

def sum_positives_before_max_abs(data):
    """Sums positive numbers located before the element with the maximum absolute value."""
    max_abs_val = abs(data[0])
    max_index = 0
    
    for i in range(1, len(data)):
        if abs(data[i]) > max_abs_val:
            max_abs_val = abs(data[i])
            max_index = i
            
    total_sum = 0
    for i in range(max_index):
        if data[i] > 0:
            total_sum += data[i]
            
    return total_sum