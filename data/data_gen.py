import json
from datetime import datetime, timedelta
import random
from typing import List, Dict

class UniversityDataGenerator:
    def __init__(self):
        self.departments = ["Computer Science", "Business", "Engineering", "Arts", "Medicine", "Law", "Economics"]
        self.event_types = ["CLASS_START", "CLASS_END", "DROP_ADD", "WITHDRAWAL", "HOLIDAY",
                          "DEADLINE", "GRADES", "ADMINISTRATIVE", "REGISTRATION", "EXAM"]
        self.sessions = ["FIRST_5_WEEK", "SECOND_5_WEEK", "FIRST_6_WEEK", "SECOND_6_WEEK",
                        "10_WEEK", "12_WEEK", "FULL_TERM"]

    def _generate_sections(self) -> List[Dict]:
        """Generate random sections for a course"""
        sections = []
        for i in range(random.randint(1, 3)):
            section = {
                "sectionId": f"SEC{str(i+1).zfill(2)}",
                "instructor": f"Professor {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Alex'])}",
                "schedule": f"{random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])} {random.randint(8,16)}:00",
                "capacity": random.randint(20, 40),
                "enrolled": random.randint(0, 20)
            }
            sections.append(section)
        return sections

    def generate_course_data(self, num_courses: int) -> List[Dict]:
        courses = []
        # First generate courses without prerequisites
        for i in range(num_courses):
            course = {
                "courseId": f"CRS{str(i+1).zfill(3)}",
                "courseName": f"Course {i+1}",
                "department": random.choice(self.departments),
                "credits": random.choice([3, 4, 6]),
                "prerequisites": [],  # Initialize empty prerequisites
                "availableSections": self._generate_sections()
            }
            courses.append(course)

        # Then add prerequisites to courses (except first-level courses)
        for i in range(num_courses):
            if i >= num_courses // 3:  # Leave first third of courses without prerequisites
                num_prereqs = random.randint(1, min(2, i))  # Ensure we don't try to add more prereqs than available
                potential_prereqs = [courses[j]["courseId"] for j in range(i)]  # Only use earlier courses as prereqs
                if potential_prereqs:  # Only add if there are potential prerequisites
                    courses[i]["prerequisites"] = random.sample(potential_prereqs, num_prereqs)

        return courses

    def generate_student_data(self, num_students: int, courses: List[Dict]) -> List[Dict]:
        students = []
        for i in range(num_students):
            # Create a proper progression of completed courses
            available_courses = courses.copy()
            completed_courses = []

            # Add courses that have no prerequisites first
            basic_courses = [course["courseId"] for course in available_courses if not course["prerequisites"]]
            if basic_courses:
                num_basic = random.randint(1, len(basic_courses))
                completed_basic = random.sample(basic_courses, num_basic)
                completed_courses.extend(completed_basic)

            # Then add some courses that have prerequisites (if their prerequisites are completed)
            advanced_courses = [course for course in available_courses
                             if course["prerequisites"] and
                             all(prereq in completed_courses for prereq in course["prerequisites"])]
            if advanced_courses:
                num_advanced = random.randint(0, min(3, len(advanced_courses)))
                completed_advanced = random.sample([course["courseId"] for course in advanced_courses], num_advanced)
                completed_courses.extend(completed_advanced)

            # Select current courses from remaining eligible courses
            eligible_current = [course["courseId"] for course in available_courses
                              if course["courseId"] not in completed_courses and
                              all(prereq in completed_courses for prereq in course["prerequisites"])]
            current_courses = random.sample(eligible_current,
                                         min(random.randint(1, 4), len(eligible_current))) if eligible_current else []

            student = {
                "studentId": f"STU{str(i+1).zfill(4)}",
                "name": f"Student {i+1}",
                "major": random.choice(self.departments),
                "completedCourses": completed_courses,
                "currentCourses": current_courses,
                "academic_standing": "Good Standing"  # Add academic standing
            }
            students.append(student)
        return students

    def generate_calendar_events(self, year: int = 2024) -> Dict:
        calendar = {
            "academicYear": f"{year}-{year+1}",
            "terms": []
        }

        for term in ["SUMMER", "FALL", "SPRING"]:
            term_data = {
                "termName": term,
                "termYear": str(year if term != "SPRING" else year + 1),
                "events": self._generate_term_events(term, year)
            }
            calendar["terms"].append(term_data)

        return calendar

    def _generate_term_events(self, term: str, year: int) -> List[Dict]:
        events = []
        start_date = datetime(year if term != "SPRING" else year + 1,
                            5 if term == "SUMMER" else 8 if term == "FALL" else 1, 1)

        # Generate regular academic events
        for i in range(30):  # Generate 30 days of events
            current_date = start_date + timedelta(days=i)
            if current_date.weekday() < 5:  # Monday to Friday
                daily_events = []

                # Add 1-3 events per day
                for _ in range(random.randint(1, 3)):
                    event_type = random.choice(self.event_types)
                    session = random.choice(self.sessions)

                    event = {
                        "eventType": event_type,
                        "description": self._generate_event_description(event_type, session),
                        "session": session
                    }

                    if event_type == "WITHDRAWAL":
                        event["refundPercentage"] = random.choice([100, 90, 80, 50, 25, 0])

                    if event_type == "HOLIDAY":
                        event["officesClosed"] = random.choice([True, False])

                    daily_events.append(event)

                events.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "dayOfWeek": current_date.strftime("%A"),
                    "events": daily_events
                })

        return events

    def _generate_event_description(self, event_type: str, session: str) -> str:
        descriptions = {
            "CLASS_START": f"Classes Begin for {session}",
            "CLASS_END": f"Classes End for {session}",
            "DROP_ADD": f"Drop/Add Period for {session}",
            "WITHDRAWAL": f"Withdrawal Period - See refund percentage",
            "HOLIDAY": random.choice(["Spring Break", "Memorial Day", "Labor Day", "Thanksgiving Break"]),
            "DEADLINE": "Important Academic Deadline",
            "GRADES": "Grade Submission Deadline",
            "ADMINISTRATIVE": "Administrative Processing Day",
            "REGISTRATION": "Course Registration Period",
            "EXAM": f"Final Exams for {session}"
        }
        return descriptions.get(event_type, "General Academic Event")

    def generate_all_data(self, num_courses: int, num_students: int):
        """Generate all university data sets"""
        courses = self.generate_course_data(num_courses)
        students = self.generate_student_data(num_students, courses)
        calendar = self.generate_calendar_events()

        return {
            "courses": courses,
            "students": students,
            "calendar": calendar
        }


# Generate development data (30 entries)
if __name__ == "__main__":
    dev_generator = UniversityDataGenerator()
    dev_data = dev_generator.generate_all_data(num_courses=30, num_students=30)

    # Generate test data (10 entries)
    test_generator = UniversityDataGenerator()
    test_data = test_generator.generate_all_data(num_courses=10, num_students=10)

    # Save development data
    with open('./dev_data.json', 'w') as f:
        json.dump(dev_data, f, indent=2)

    # Save test data
    with open('./test_data.json', 'w') as f:
        json.dump(test_data, f, indent=2)
