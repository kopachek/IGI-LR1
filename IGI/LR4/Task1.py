import csv
import pickle

class Student:
    """Class to store student information."""
    def __init__(self, surname, needs_dorm, experience, education, language):
        self.surname = surname
        self.needs_dorm = bool(needs_dorm)
        self.experience = int(experience)
        self.education = education
        self.language = language

    def __repr__(self):
        return (f"Student(surname='{self.surname}', dorm={self.needs_dorm}, "
                f"exp={self.experience}, edu='{self.education}', lang='{self.language}')")
    
    def __str__(self):
        return(f"Surname: {self.surname}\nNeeds dorm: {self.needs_dorm}\nExpirience: {self.experience}\nEducation: {self.education}\nLanguage: {self.language}\n")
    
    @staticmethod
    def fmt_from_dict(s):
        return(f"Surname: {s["surname"]}\nNeeds dorm: {s["needs_dorm"]}\nExpirience: {s["experience"]}\nEducation: {s["education"]}\nLanguage: {s["language"]}\n")

class StudentManager:
    """Class for managing student list, serialization, and data processing."""
    @staticmethod
    def save_to_csv(filename, students):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            columns = ["surname","needs_dorm","experience","education","language"]
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(students)

    @staticmethod
    def load_from_csv(filename):
        students_dict = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students_dict.append(row)
        return students_dict

    @staticmethod
    def save_to_pickle(filename, students):
        with open(filename, 'wb') as f:
            pickle.dump(students, f)

    @staticmethod
    def load_from_pickle(filename):
        students = []
        with open(filename, 'rb') as f:
            students = pickle.load(f)
        return students

    @staticmethod
    def count_needing_dorm(students):
        return sum(1 for s in students if s["needs_dorm"])

    @staticmethod
    def get_experienced_students(students, years):
        return [s for s in students if s["experience"] > years]

    @staticmethod
    def get_students_by_education(students, edu_type):
        return [s for s in students if s["education"].lower() == edu_type.lower()]

    @staticmethod
    def group_by_language(students):
        groups = {}
        for s in students:
            if s["language"] not in groups:
                groups[s["language"]] = []
            groups[s["language"]].append(s)
        return groups

    @staticmethod
    def search_by_surname(students, surname):
        return [s for s in students if s["surname"].lower() == surname.lower()]

def task_1():
    students = [
        {"surname": "Ivanov", "needs_dorm": True, "experience": 3, "education": "college", "language": "English"},
        {"surname": "Petrov", "needs_dorm": False, "experience": 1, "education": "technical school", "language": "German"},
        {"surname": "Sidorov", "needs_dorm": True, "experience": 5, "education": "technical school", "language": "English"},
        {"surname": "Smith", "needs_dorm": False, "experience": 0, "education": "high school", "language": "French"}
    ]

    StudentManager.save_to_csv("T1\\students.csv", students)
    StudentManager.save_to_pickle("T1\\students.pkl", students)

    students = StudentManager.load_from_pickle("T1\\students.pkl")

    print(f"a) Number of students needing a dormitory: {StudentManager.count_needing_dorm(students)}")

    print("\nb) Students with more than 2 years of experience:")
    for s in StudentManager.get_experienced_students(students, 2):
        print(Student.fmt_from_dict(s))

    print("\nc) Students who graduated from technical school:")
    for s in StudentManager.get_students_by_education(students, "technical school"):
        print(Student.fmt_from_dict(s))

    print("\nd) Language groups:")
    for lang, stud in StudentManager.group_by_language(students).items():
        print(f"{lang}: {[s["surname"] for s in stud]}")

    search_name = input("\nEnter surname to search: ")
    for s in StudentManager.search_by_surname(students, search_name):
        print(Student.fmt_from_dict(s))

if __name__ == "__main__":
    task_1()