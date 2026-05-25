def count_in_range(sequence):
    """Counts elements in the sequence within the range [5, 25]."""
    count = 0
    for number in sequence:
        if 5 <= number <= 25:
            count += 1
    return count

def get_int_sequence():
    """Reads integers from input until zero is entered, with error handling."""
    numbers = []

    while True:
        try:
            val = int(input())
            if val == 0:
                break
            numbers.append(val)
        except ValueError:
            print("Error: integer required")
    return numbers