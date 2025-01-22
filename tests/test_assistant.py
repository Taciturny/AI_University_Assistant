import unittest
from src.assistant import UniversityAssistant
from src.utils import format_course_info, calculate_gpa
import os

# class TestUniversityAssistant(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         api_key = os.getenv("COHERE_API_KEY")
#         cls.assistant = UniversityAssistant(api_key, "./data/test_data.json")

#     def test_course_recommendations(self):
#         recommendations = self.assistant.get_course_recommendations("STU0001")
#         self.assertIsInstance(recommendations, list)
#         self.assertLessEqual(len(recommendations), 5)

#     def test_deadline_check(self):
#         deadlines = self.assistant.check_upcoming_deadlines("FULL_TERM")
#         self.assertIsInstance(deadlines, list)
#         self.assertLessEqual(len(deadlines), 5)

#     def test_registration_eligibility(self):
#         result = self.assistant.verify_registration_eligibility("STU0001", "CRS001")
#         self.assertIsInstance(result, dict)
#         self.assertIn("eligible", result)

#     def test_format_course_info(self):
#         course = self.assistant.data["courses"][0]
#         formatted = format_course_info(course)
#         self.assertIsInstance(formatted, str)
#         self.assertIn(course["courseId"], formatted)

#     def test_calculate_gpa(self):
#         student = self.assistant.data["students"][0]
#         gpa = calculate_gpa(student["completedCourses"], self.assistant.data["courses"])
#         self.assertIsInstance(gpa, float)
#         self.assertGreaterEqual(gpa, 0.0)
#         self.assertLessEqual(gpa, 4.0)

# if __name__ == '__main__':
#     unittest.main()


# # tests/test_assistant.py
# import unittest
# from datetime import datetime, timedelta
# import json
# import os

# from src.assistant import UniversityAssistant

# class TestUniversityAssistant(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Load test data
#         with open('./data/test_data.json', 'r') as f:
#             cls.test_data = json.load(f)

#         # Initialize assistant with test data
#         cls.assistant = UniversityAssistant(os.getenv('COHERE_API_KEY'))
#         cls.assistant.load_data(cls.test_data)

#     def test_get_student_info(self):
#         # Test with first student in test data
#         student_id = self.test_data['students'][0]['studentId']
#         info = self.assistant.get_student_info(student_id)

#         self.assertIsNotNone(info)
#         self.assertIn('student', info)
#         self.assertIn('courses', info)

#     def test_upcoming_events(self):
#         events = self.assistant.get_upcoming_events(days=30)
#         self.assertIsInstance(events, list)

#     def test_prerequisite_check(self):
#         # Test with first student and a course
#         student_id = self.test_data['students'][0]['studentId']
#         course_id = self.test_data['courses'][0]['courseId']

#         result = self.assistant.check_prerequisites(student_id, course_id)
#         self.assertIsInstance(result, dict)
#         self.assertIn('eligible', result)

# # Example usage script
# def example_usage():
#     # Initialize assistant
#     assistant = create_assistant(os.getenv('COHERE_API_KEY'))

#     # Example 1: Course Registration Query
#     student_id = "STU0001"
#     query = "I want to register for Computer Science courses. What are my options?"
#     response = assistant.handle_registration_query(student_id, query)
#     print("Registration Query Response:", response)

#     # Example 2: Deadline Query
#     query = "What are the important deadlines for the next month?"
#     response = assistant.handle_deadline_query(query)
#     print("Deadline Query Response:", response)

#     # Example 3: Check Prerequisites
#     course_id = "CRS001"
#     result = assistant.check_prerequisites(student_id, course_id)
#     print("Prerequisite Check Result:", result)

# if __name__ == '__main__':
#     # Run tests
#     unittest.main(argv=['first-arg-is-ignored'], exit=False)

#     # Run example usage
#     example_usage()




import unittest
from unittest.mock import Mock, patch
import json
import os
from datetime import datetime

# Import your actual classes
from university_assistant import UniversityAssistant
from data_generator import UniversityDataGenerator

class TestUniversityAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate test data
        generator = UniversityDataGenerator()
        cls.test_data = generator.generate_all_data(num_courses=5, num_students=3)

        # Save test data temporarily
        with open('test_data_temp.json', 'w') as f:
            json.dump(cls.test_data, f)

        # Initialize assistant with test data
        cls.assistant = UniversityAssistant("test-api-key", "test_data_temp.json")

    @classmethod
    def tearDownClass(cls):
        # Clean up temporary test file
        if os.path.exists('test_data_temp.json'):
            os.remove('test_data_temp.json')

    def test_get_course_recommendations(self):
        # Test course recommendations
        recommendations = self.assistant.get_course_recommendations("STU0001")
        self.assertIsInstance(recommendations, list)
        if recommendations:  # If student exists and has recommendations
            self.assertIsInstance(recommendations[0], dict)
            self.assertIn('courseId', recommendations[0])

    def test_check_upcoming_deadlines(self):
        # Test deadline checking
        deadlines = self.assistant.check_upcoming_deadlines("FULL_TERM")
        self.assertIsInstance(deadlines, list)
        if deadlines:
            self.assertIn('date', deadlines[0])
            self.assertIn('type', deadlines[0])

    def test_verify_registration_eligibility(self):
        # Test registration eligibility
        result = self.assistant.verify_registration_eligibility("STU0001", "CRS001")
        self.assertIsInstance(result, dict)
        self.assertIn('eligible', result)

    def test_calculate_gpa(self):
        # Test GPA calculation
        student = self.assistant._find_student("STU0001")
        if student:
            gpa = self.assistant.calculate_gpa(student["completedCourses"], self.test_data["courses"])
            self.assertIsInstance(gpa, float)
            self.assertTrue(0.0 <= gpa <= 4.0)

    def test_invalid_student_id(self):
        # Test handling of invalid student ID
        result = self.assistant.get_course_recommendations("INVALID_ID")
        self.assertEqual(result, [])

    def test_invalid_course_id(self):
        # Test handling of invalid course ID
        result = self.assistant.verify_registration_eligibility("STU0001", "INVALID_COURSE")
        self.assertFalse(result["eligible"])

class TestUniversityDataGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = UniversityDataGenerator()

    def test_generate_course_data(self):
        courses = self.generator.generate_course_data(5)
        self.assertEqual(len(courses), 5)
        self.assertIn('courseId', courses[0])
        self.assertIn('prerequisites', courses[0])

    def test_generate_student_data(self):
        courses = self.generator.generate_course_data(5)
        students = self.generator.generate_student_data(3, courses)
        self.assertEqual(len(students), 3)
        self.assertIsInstance(students[0]['completedCourses'], dict)  # Test for grade dictionary

    def test_generate_calendar_events(self):
        calendar = self.generator.generate_calendar_events()
        self.assertIn('terms', calendar)
        self.assertGreater(len(calendar['terms']), 0)

if __name__ == '__main__':
    unittest.main()
