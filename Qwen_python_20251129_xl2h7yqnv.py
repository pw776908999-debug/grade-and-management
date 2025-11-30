

import json
import os
from typing import List, Dict, Optional


class Student:
    """Represents a single student with ID, name, and grades."""
    
    def __init__(self, student_id: str, name: str, grades: List[float] = None):
        self.student_id = student_id
        self.name = name
        self.grades = grades if grades is not None else []

    def add_grade(self, grade: float):
        """Add a grade (must be between 0 and 100)."""
        if 0 <= grade <= 100:
            self.grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100.")

    def calculate_average(self) -> float:
        """Return the average of all grades. Returns 0 if no grades."""
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

    def get_performance(self) -> str:
        """Return performance label based on average."""
        avg = self.calculate_average()
        if avg >= 90: return "Excellent"
        if avg >= 80: return "Good"
        if avg >= 70: return "Average"
        if avg >= 60: return "Below Average"
        return "Poor"

    def to_dict(self) -> dict:
        """Convert student to a dictionary (for saving to JSON)."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Student from a dictionary (for loading from JSON)."""
        return cls(data["student_id"], data["name"], data["grades"])

    def __str__(self):
        avg = self.calculate_average()
        return f"ID: {self.student_id} | Name: {self.name} | Avg: {avg:.2f}"


class StudentManagementSystem:
    """Manages all student records with file saving, search, sort, and reporting."""

    def __init__(self, data_file: str = "students.json"):
        self.data_file = data_file
        self.students: Dict[str, Student] = {}
        self.load_data()

    def load_data(self):
        """Load students from JSON file (if it exists)."""
        if not os.path.exists(self.data_file):
            print("✅ No existing data found. Starting fresh!")
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for item in data:
                    student = Student.from_dict(item)
                    self.students[student.student_id] = student
            print(f"✅ Loaded {len(self.students)} student(s) from '{self.data_file}'.")
        except Exception as e:
            print(f"⚠️ Warning: Could not load data from '{self.data_file}': {e}")
            print("Starting with empty database.")

    def save_data(self):
        """Save all students to JSON file."""
        try:
            with open(self.data_file, "w") as f:
                json.dump(
                    [s.to_dict() for s in self.students.values()],
                    f,
                    indent=4
                )
            print("💾 Data saved successfully!")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def register_student(self):
        """Interactive student registration."""
        print("\n📝 Register a New Student")
        student_id = input("Enter Student ID (e.g., S101): ").strip()
        if not student_id:
            print("❌ ID cannot be empty!")
            return

        if student_id in self.students:
            print("❌ Student ID already exists!")
            return

        name = input("Enter Student Name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return

        self.students[student_id] = Student(student_id, name)
        self.save_data()
        print(f"✅ Student '{name}' registered successfully!")

    def add_grade(self):
        """Add a grade to an existing student."""
        print("\n➕ Add Grade")
        student_id = input("Enter Student ID: ").strip()
        if student_id not in self.students:
            print("❌ Student not found!")
            return

        try:
            grade = float(input("Enter Grade (0–100): "))
            self.students[student_id].add_grade(grade)
            self.save_data()
            print(f"✅ Grade {grade} added to {self.students[student_id].name}.")
        except ValueError as e:
            print(f"❌ Invalid grade: {e}")

    def display_performance_report(self):
        """Show performance report for one or all students."""
        print("\n📊 Performance Report")
        choice = input("View (1) All Students or (2) One Student? (1/2): ").strip()

        if choice == "2":
            sid = input("Enter Student ID: ").strip()
            if sid not in self.students:
                print("❌ Student not found!")
                return
            students = [self.students[sid]]
        elif choice == "1":
            if not self.students:
                print("📭 No students to display.")
                return
            students = list(self.students.values())
        else:
            print("❌ Invalid choice.")
            return

        print("\n" + "="*70)
        print(f"{'Student Performance Report'.center(70)}")
        print("="*70)
        print(f"{'ID':<12} {'Name':<20} {'Average':<10} {'Performance'}")
        print("-"*70)
        for s in students:
            avg = s.calculate_average()
            perf = s.get_performance()
            print(f"{s.student_id:<12} {s.name:<20} {avg:<10.2f} {perf}")
        print("="*70)

    def search_student(self):
        """Search students by ID or name."""
        print("\n🔍 Search Student")
        query = input("Enter ID or Name to search: ").strip().lower()
        if not query:
            print("❌ Search query cannot be empty.")
            return

        results = [
            s for s in self.students.values()
            if query in s.student_id.lower() or query in s.name.lower()
        ]

        if results:
            print(f"\n✅ Found {len(results)} result(s):")
            for s in results:
                print(f" - {s}")
        else:
            print("📭 No matching students found.")

    def display_all_students(self):
        """List all students with grades."""
        if not self.students:
            print("\n📭 No students registered yet.")
            return

        print("\n" + "="*80)
        print(f"{'All Students'.center(80)}")
        print("="*80)
        print(f"{'ID':<12} {'Name':<20} {'Grades':<35} {'Avg'}")
        print("-"*80)
        for s in self.students.values():
            grades_str = ", ".join(str(g) for g in s.grades) if s.grades else "—"
            avg = s.calculate_average()
            print(f"{s.student_id:<12} {s.name:<20} {grades_str:<35} {avg:.2f}")
        print("="*80)

    def sort_and_display(self):
        """Sort students and display."""
        if not self.students:
            print("\n📭 No students to sort.")
            return

        print("\n🔢 Sort Students By:")
        print("1. Student ID")
        print("2. Name")
        print("3. Average Grade")
        choice = input("Choose (1-3): ").strip()

        reverse = input("Descending order? (y/n): ").strip().lower() == "y"

        students_list = list(self.students.values())

        if choice == "1":
            students_list.sort(key=lambda s: s.student_id, reverse=reverse)
        elif choice == "2":
            students_list.sort(key=lambda s: s.name.lower(), reverse=reverse)
        elif choice == "3":
            students_list.sort(key=lambda s: s.calculate_average(), reverse=reverse)
        else:
            print("❌ Invalid choice. Showing unsorted list.")
            return

        print("\n" + "="*80)
        print(f"{'Sorted Students'.center(80)}")
        print("="*80)
        print(f"{'ID':<12} {'Name':<20} {'Grades':<35} {'Avg'}")
        print("-"*80)
        for s in students_list:
            grades_str = ", ".join(str(g) for g in s.grades) if s.grades else "—"
            avg = s.calculate_average()
            print(f"{s.student_id:<12} {s.name:<20} {grades_str:<35} {avg:.2f}")
        print("="*80)


def main():
    print("🎓 Welcome to the Student Management System!")
    print("Your data will be saved in 'students.json'")
    sms = StudentManagementSystem()

    while True:
        print("\n" + "—"*50)
        print("MAIN MENU")
        print("—"*50)
        print("1. 📝 Register Student")
        print("2. ➕ Add Grade")
        print("3. 📊 View Performance Report")
        print("4. 🔍 Search Student")
        print("5. 👥 View All Students")
        print("6. 🔢 Sort & View Students")
        print("7. 🚪 Exit")

        choice = input("\n👉 Choose an option (1-7): ").strip()

        if choice == "1":
            sms.register_student()
        elif choice == "2":
            sms.add_grade()
        elif choice == "3":
            sms.display_performance_report()
        elif choice == "4":
            sms.search_student()
        elif choice == "5":
            sms.display_all_students()
        elif choice == "6":
            sms.sort_and_display()
        elif choice == "7":
            print("\n👋 Thank you for using the Student Management System!")
            break
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()