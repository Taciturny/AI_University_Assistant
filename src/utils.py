import logging
from typing import Dict, List
from datetime import datetime
logger = logging.getLogger(__name__)



def format_course_info(course: Dict) -> str:
    """Format course information with error handling"""
    try:
        prerequisites = course.get("prerequisites", [])
        prereq_text = ', '.join(prerequisites) if prerequisites else 'None'

        sections_info = "\n".join([
            f"Section {s['sectionId']}: {s['schedule']} with {s['instructor']} "
            f"({s['enrolled']}/{s['capacity']} enrolled)"
            for s in course.get("availableSections", [])
        ])

        return f"""
Course: {course.get('courseName', 'N/A')} ({course.get('courseId', 'N/A')})
Department: {course.get('department', 'N/A')}
Credits: {course.get('credits', 'N/A')}
Prerequisites: {prereq_text}
Available Sections:
{sections_info}
"""
    except Exception as e:
        logger.error(f"Error formatting course info: {str(e)}")
        return "Error formatting course information"


def format_deadline_info(deadline: Dict) -> str:
    """Format deadline information for display"""
    return f"""
Date: {deadline['date']}
Type: {deadline['type']}
Description: {deadline['description']}
"""

def get_next_term_dates(calendar_data: Dict) -> Dict:
    """Get the start and end dates for the next term"""
    current_date = datetime.now()

    for term in calendar_data["terms"]:
        term_events = sorted(term["events"], key=lambda x: x["date"])
        term_start = datetime.strptime(term_events[0]["date"], "%Y-%m-%d")
        term_end = datetime.strptime(term_events[-1]["date"], "%Y-%m-%d")

        if term_start > current_date:
            return {
                "term": term["termName"],
                "start_date": term_events[0]["date"],
                "end_date": term_events[-1]["date"]
            }

    return None

def calculate_gpa(completed_courses: List[str], courses_data: List[Dict]) -> float:
    """Calculate student's GPA based on completed courses"""
    # This is a simplified GPA calculation
    total_credits = 0
    total_grade_points = 0

    # Mock grades for demonstration - in real system, would come from student records
    grade_points = {
        "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "F": 0.0
    }

    for course_id in completed_courses:
        course = next((c for c in courses_data if c["courseId"] == course_id), None)
        if course:
            # Simulate a grade - in real system, would use actual grade
            grade = list(grade_points.keys())[hash(course_id) % len(grade_points)]
            credits = course["credits"]
            total_credits += credits
            total_grade_points += credits * grade_points[grade]

    return round(total_grade_points / total_credits, 2) if total_credits > 0 else 0.0



# from typing import Dict, List, Optional
# from datetime import datetime, timedelta

# def format_date(date_str: str) -> str:
#     """Convert date string to formatted date"""
#     date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#     return date_obj.strftime('%B %d, %Y')

# def filter_events_by_type(events: List[Dict], event_types: Optional[List[str]] = None) -> List[Dict]:
#     """Filter events by type"""
#     if not event_types:
#         return events

#     filtered = []
#     for event in events:
#         filtered_daily_events = [
#             e for e in event['events']
#             if e['eventType'] in event_types
#         ]
#         if filtered_daily_events:
#             event_copy = event.copy()
#             event_copy['events'] = filtered_daily_events
#             filtered.append(event_copy)
#     return filtered

# def check_schedule_conflict(schedule1: str, schedule2: str) -> bool:
#     """Check if two schedules conflict"""
#     # Simple implementation - can be enhanced
#     return schedule1 == schedule2
