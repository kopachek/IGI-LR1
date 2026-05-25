import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import os
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class ShapeColor:
    def __init__(self, color_name):
        self._color = color_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

class DrawableTrapezoidMixin:
    def draw(self, label_text, filename):
        h = self.b * math.sin(self.y_rad)
        x_offset = self.b * math.cos(self.y_rad)

        vertices = [
            [0, 0],
            [self.a, 0],
            [self.a - x_offset, h],
            [x_offset, h]
        ]
        
        fig, ax = plt.subplots()
        polygon = patches.Polygon(vertices, closed=True, 
                                  linewidth=2, edgecolor='black', 
                                  facecolor=self.color_obj.color)
        ax.add_patch(polygon)
        
        ax.set_xlim(-1, self.a + 1)
        ax.set_ylim(-1, h + 1)
        ax.set_aspect('equal')
        
        plt.text(self.a/2, h/2, label_text, ha='center', fontweight='bold')

        folder, filename = os.path.split(filename)

        if not os.path.exists(folder):
            os.makedirs(folder)

        full_path = os.path.join(folder, filename)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.show()

class IsoscelesTrapezoid(Shape, DrawableTrapezoidMixin):
    def __init__(self, base_a, side_b, angle_y, color_name):
        self.name = "Isosceles Trapezoid"
        self.a = base_a
        self.b = side_b
        self.y_deg = angle_y
        self.y_rad = math.radians(angle_y)
        self.color_obj = ShapeColor(color_name)

    def calculate_area(self):
        h = self.b * math.sin(self.y_rad)
        c = self.a - 2 * (self.b * math.cos(self.y_rad))
        return ((self.a + c) / 2) * h

    def get_info(self):
        info = "Shape: {0}, Color: {1}, Base: {2}, Side: {3}, Angle: {4} deg, Area: {5:.2f}"
        return info.format(self.name, self.color_obj.color, self.a, self.b, self.y_deg, self.calculate_area())

    def get_name(self):
        return self.name

def task_4(out_name):
    try:
        a = float(input("Bottom base (a): "))
        b = float(input("Side(b): "))
        y = float(input("Angle between the base and the side(Y): "))
        user_color = input("Color: ")
        user_label = input("Label text: ")

        if y >= 180 or y <= 0 or (2 * b * math.cos(math.radians(y)) >= a):
            raise ValueError("Impossible trapezoid angle.")
        else:
            trapezoid = IsoscelesTrapezoid(a, b, y, user_color)
            print("\n" + trapezoid.get_info())
            trapezoid.draw(user_label, out_name)
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    task_4("T4\\trapezoid.png")