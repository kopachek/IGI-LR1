import os
from circle import area

def main():
    radius_str = os.getenv("RADIUS", "0")
    
    try:
        radius = float(radius_str)
        result = area(radius)
        print(f"При радиусе {radius}, площадь круга равна: {result}")
    except ValueError:
        print("Ошибка: Переменная RADIUS должна быть числом.")

if __name__ == "__main__":
    main()