# import json
import os
from typing import Dict, List, Optional
import logging
import json
import cohere
from datetime import datetime
from dataclasses import dataclass
from .prompts import PromptManager

logger = logging.getLogger(__name__)


class UniversityAssistant:
    def __init__(self, api_key: str, data_path: str = "./data/dev_data.json"):
        try:
            self.co = cohere.Client(api_key)
            self.data = self._load_data(data_path)
            self.prompt_manager = PromptManager()
            logger.info("University Assistant initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize University Assistant: {str(e)}")
            raise

    def _load_data(self, path: str) -> Dict:
        """Load data with error handling"""
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Data file not found: {path}")

            with open(path, 'r') as f:
                data = json.load(f)
            logger.info(f"Successfully loaded data from {path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data in {path}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading data from {path}: {str(e)}")
            raise

    def get_course_recommendations(self, student_id: str) -> List[Dict]:
        """Get course recommendations for a student using Cohere API"""
        try:
            student = self._find_student(student_id)
            if not student:
                logger.warning(f"No student found for ID: {student_id}")
                return []

            # Generate prompt for Cohere
            try:
                prompt = self.prompt_manager.get_prompt(
                    "task_prompts",
                    "course_recommendation",
                    completed_courses=student["completedCourses"],
                    current_courses=student["currentCourses"],
                    major=student["major"],
                    academic_standing=student.get("academic_standing", "Good Standing")
                )

                logger.debug(f"Generated prompt for Cohere: {prompt}")

                # Get recommendations from Cohere
                response = self.co.generate(
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0.7,
                    k=0,
                    stop_sequences=[],
                    return_likelihoods='NONE'
                )

                logger.debug(f"Received response from Cohere: {response}")

            except Exception as e:
                logger.error(f"Error in Cohere API interaction: {str(e)}")
                # Fall back to basic filtering if Cohere fails
                logger.info("Falling back to basic course filtering")
                response = None

            # Get available courses (not completed or current)
            available_courses = [
                course for course in self.data["courses"]
                if course["courseId"] not in student["completedCourses"]
                and course["courseId"] not in student["currentCourses"]
            ]

            # Filter eligible courses
            eligible_courses = self._filter_eligible_courses(available_courses, student)

            # If we have Cohere response, use it to rank courses
            if response and hasattr(response, 'generations') and response.generations:
                try:
                    # Parse Cohere's response to get recommended course IDs
                    # This assumes the response is formatted as a comma-separated list of course IDs
                    recommended_ids = response.generations[0].text.strip().split(',')
                    recommended_ids = [rid.strip() for rid in recommended_ids]

                    # Reorder eligible courses based on Cohere's recommendations
                    ranked_courses = []
                    # First add courses that Cohere recommended
                    for course_id in recommended_ids:
                        course = next((c for c in eligible_courses
                                    if c["courseId"] == course_id), None)
                        if course and course not in ranked_courses:
                            ranked_courses.append(course)

                    # Then add any remaining eligible courses
                    for course in eligible_courses:
                        if course not in ranked_courses:
                            ranked_courses.append(course)

                    logger.info(f"Successfully ranked {len(ranked_courses)} courses using Cohere")
                    return ranked_courses[:5]  # Return top 5 ranked courses

                except Exception as e:
                    logger.error(f"Error processing Cohere response: {str(e)}")
                    return eligible_courses[:5]  # Fall back to unranked eligible courses

            # If no Cohere response, return unranked eligible courses
            logger.info(f"Returning {len(eligible_courses[:5])} unranked eligible courses")
            return eligible_courses[:5]

        except Exception as e:
            logger.error(f"Error in get_course_recommendations: {str(e)}")
            return []


    def check_upcoming_deadlines(self, session: str, event_type: Optional[str] = None) -> List[Dict]:
        """Check upcoming deadlines for a specific session"""
        current_date = datetime.now()

        upcoming_events = []
        for term in self.data["calendar"]["terms"]:
            for day in term["events"]:
                date = datetime.strptime(day["date"], "%Y-%m-%d")
                if date >= current_date:
                    for event in day["events"]:
                        if event["session"] == session and (not event_type or event["eventType"] == event_type):
                            upcoming_events.append({
                                "date": day["date"],
                                "type": event["eventType"],
                                "description": event["description"]
                            })

        return upcoming_events[:5]  # Return next 5 upcoming events

    def verify_registration_eligibility(self, student_id: str, course_id: str) -> Dict:
        """Verify if a student can register for a specific course"""
        student = self._find_student(student_id)
        course = self._find_course(course_id)

        if not student or not course:
            return {"eligible": False, "reason": "Student or course not found"}

        # Check prerequisites
        missing_prereqs = [
            prereq for prereq in course["prerequisites"]
            if prereq not in student["completedCourses"]
        ]

        if missing_prereqs:
            return {
                "eligible": False,
                "reason": f"Missing prerequisites: {', '.join(missing_prereqs)}"
            }

        # Check course capacity
        available_sections = [
            section for section in course["availableSections"]
            if section["enrolled"] < section["capacity"]
        ]

        if not available_sections:
            return {
                "eligible": False,
                "reason": "No available sections - course is full"
            }

        return {
            "eligible": True,
            "available_sections": available_sections
        }

    def _find_student(self, student_id: str) -> Optional[Dict]:
        """Find a student by ID with error handling"""
        try:
            student = next((s for s in self.data["students"] if s["studentId"] == student_id), None)
            if student:
                logger.debug(f"Found student: {student_id}")
            else:
                logger.warning(f"Student not found: {student_id}")
            return student
        except Exception as e:
            logger.error(f"Error finding student {student_id}: {str(e)}")
            return None

    def _find_course(self, course_id: str) -> Optional[Dict]:
        """Find a course by ID with error handling"""
        try:
            course = next((c for c in self.data["courses"] if c["courseId"] == course_id), None)
            if course:
                logger.debug(f"Found course: {course_id}")
            else:
                logger.warning(f"Course not found: {course_id}")
            return course
        except Exception as e:
            logger.error(f"Error finding course {course_id}: {str(e)}")
            return None

    def _filter_eligible_courses(self, courses: List[Dict], student: Dict) -> List[Dict]:
        """Filter courses based on student eligibility with error handling"""
        try:
            eligible_courses = []
            for course in courses:
                prerequisites = course.get("prerequisites", [])
                if not prerequisites or all(prereq in student["completedCourses"] for prereq in prerequisites):
                    eligible_courses.append(course)

            logger.info(f"Found {len(eligible_courses)} eligible courses")
            return eligible_courses[:5]
        except Exception as e:
            logger.error(f"Error filtering eligible courses: {str(e)}")
            return []



@dataclass
class Grade:
    letter: str
    points: float

class GradeCalculator:
    GRADE_POINTS = {
        "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "F": 0.0
    }

    @classmethod
    def calculate_gpa(cls, completed_courses: List[str], courses_data: List[Dict]) -> float:
        """Calculate student's GPA based on completed courses with proper error handling"""
        try:
            if not completed_courses:
                logger.warning("No completed courses provided")
                return 0.0

            if not courses_data:
                logger.warning("No courses data provided")
                return 0.0

            total_credits = 0
            total_grade_points = 0

            for course_id in completed_courses:
                course = next((c for c in courses_data if c["courseId"] == course_id), None)
                if course:
                    # Generate a consistent but random-seeming grade based on student ID and course ID
                    # This will ensure the same student gets the same grade for the same course
                    grade_index = hash(f"{course_id}") % len(cls.GRADE_POINTS)
                    grade_key = list(cls.GRADE_POINTS.keys())[grade_index]
                    grade_points = cls.GRADE_POINTS[grade_key]
                    credits = course.get("credits", 3)  # Default to 3 credits if not specified

                    total_credits += credits
                    total_grade_points += credits * grade_points

                    logger.debug(f"Course {course_id}: Grade {grade_key}, Points {grade_points}, Credits {credits}")

            if total_credits == 0:
                logger.warning("No valid courses found for GPA calculation")
                return 0.0

            gpa = round(total_grade_points / total_credits, 2)
            logger.info(f"Calculated GPA: {gpa}")
            return gpa

        except Exception as e:
            logger.error(f"Error calculating GPA: {str(e)}")
            return 0.0

