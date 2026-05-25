import random

def init_from_user():
    """Prompts for count and individual float values with error handling."""
    result = []
    
    while True:
        try:
            count = int(input("Enter elements count: "))
            if count <= 0:
                print("Error: positive integer required")
                continue
            break
        except ValueError:
            print("Error: integer required")
    
    print(f"Enter {count} float numbers:")
    
    for i in range(count):
        while True:
            try:
                value = float(input())
                result.append(value)
                break
            except ValueError:
                print("Error: number required")
    
    return result


def init_with_generator():
    """Generates a sequence of random floats based on user-defined count."""
    while True:
        try:
            count = int(input("Enter elements count: "))
            if count <= 0:
                print("Error: positive integer required")
                continue
            break
        except ValueError:
            print("Error: integer required")

    for _ in range(count):
        yield random.uniform(-10e4, 10e4)