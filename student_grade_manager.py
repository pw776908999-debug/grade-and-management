import os
import sys

STUDENTS_FILE = "students.txt"

class Student:
    def __init__(self, student_id, name, grades=None):
        self.student_id = student_id
        self.name = name
        self.grades = grades if grades else []

    def average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def status(self):
        avg = self.average()
        return "PASS" if avg >= 50 else "FAIL"

    def to_record(self):
        return f"{self.student_id}|{self.name}|{','.join(map(str, self.grades))}\n"

    @staticmethod
    def from_record(record_line):
        parts = record_line.strip().split('|')
        sid, name = parts[0], parts[1]
        grades = list(map(float, parts[2].split(','))) if len(parts) > 2 and parts[2] else []
        return Student(sid, name, grades)

def load_students():
    students = []
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "r") as f:
            for line in f:
                try:
                    student = Student.from_record(line)
                    students.append(student)
                except Exception as e:
                    print(f"Error loading a student record: {e}")
    return students

def save_students(students):
    with open(STUDENTS_FILE, "w") as f:
        for student in students:
            f.write(student.to_record())

def register_student(students):
    try:
        sid = input("Enter student ID: ")
        if any(s.student_id == sid for s in students):
            print("Student ID already exists. Registration cancelled.")
            return
        name = input("Enter student name: ")
        students.append(Student(sid, name))
        print(f"Student {name} registered successfully.")
    except Exception as e:
        print(f"Registration failed: {e}")

def input_grades(students):
    sid = input("Enter student ID to input grades: ")
    student = next((s for s in students if s.student_id == sid), None)
    if not student:
        print("Student not found.")
        return
    try:
        grades_str = input("Enter grades separated by spaces: ")
        grades = list(map(float, grades_str.strip().split()))
        student.grades.extend(grades)
        print(f"Grades updated for {student.name}.")
    except Exception as e:
        print(f"Invalid input: {e}")

def display_report(students):
    if not students:
        print("No students registered yet.")
        return
    print("\n=== Performance Report ===")
    print("{:<8} {:<15} {:<20} {:<10} {:<10}".format("ID", "Name", "Grades", "Average", "Status"))
    print("-" * 65)
    for s in students:
        grades_str = ', '.join(map(lambda x: "%.1f" % x, s.grades))
        print("{:<8} {:<15} {:<20} {:<10.2f} {:<10}".format(
            s.student_id, s.name, grades_str, s.average(), s.status()))
    print()

def search_student(students):
    try:
        name = input("Enter student name to search for: ").lower()
        found = [s for s in students if name in s.name.lower()]
        if not found:
            print("No students matched that name.")
        else:
            for s in found:
                grades_str = ', '.join(map(str, s.grades))
                print(f"ID: {s.student_id}, Name: {s.name}, Grades: {grades_str}, Average: {s.average():.2f}, Status: {s.status()}")
    except Exception as e:
        print(f"Search failed: {e}")

def sort_students(students):
    print("Sort by: 1. Name 2. Average Grade")
    choice = input("Choose option (1/2): ")
    if choice == "1":
        students.sort(key=lambda x: x.name.lower())
        print("Sorted by name.")
    elif choice == "2":
        students.sort(key=lambda x: x.average(), reverse=True)
        print("Sorted by average grade (descending).")
    else:
        print("Invalid sort choice.")

def main_menu():
    students = load_students()
    while True:
        print("""
===== Student Grade Manager =====
1. Register Student
2. Input Grades
3. Compute & Display Performance Report
4. Search Student
5. Sort Students
6. Save and Exit
        """)
        choice = input("Select an option (1-6): ")
        try:
            if choice == '1':
                register_student(students)
            elif choice == '2':
                input_grades(students)
            elif choice == '3':
                display_report(students)
            elif choice == '4':
                search_student(students)
            elif choice == '5':
                sort_students(students)
            elif choice == '6':
                save_students(students)
                print("All changes saved. Goodbye!")
                break
            else:
                print("Unknown option, try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the Student Grade Management System.")
    main_menu()