
``` bash
university_assistant/
|── main.py|
├── data/
|   ├── dev_data.json
│   ├── dev_data.json
│   └── test_data.json
├── docs/
│   ├── prompts/
│   │   └── base_prompts.json
│   └── diagrams/
├── src/
│   ├── __init__.py
│   ├── assistant.py       # Main assistant code
│   └── utils.py          # Utility functions
└── tests/
    ├── __init__.py
    └── test_assistant.py
```


# University Assistant System Documentation

Goal: Develop an AI assistant that helps students with daily tasks such as course registration, assignment deadlines, and campus event updates.



Overall Project Structure
![Project Architecture](https://github.com/Taciturny/AI_University_Assistant/blob/main/university_screenshots/simple_arch.png)


## 1. System Overview

The University Assistant is an AI-powered system designed to help students with course registration, academic planning, and administrative tasks. The system integrates traditional university workflows with modern AI capabilities through Cohere's language models.

### 1.1 Core Components

- **AI University Assistant Core**: Central system that coordinates between different agents and interfaces
- **Command Line Interface**: Primary user interaction point for students
- **API Interface**: External system integration point
- **Three Specialized Agents**:
  - Registration Agent
  - Calendar Agent
  - Student Query Agent

You can explore the codebase of synthetic data generation in the [data folder](https://github.com/Taciturny/AI_University_Assistant/blob/main/data/data_gen.py)


### 1.2 Data Management

The system handles three primary data types:
- Student Data
- Course Data
- Calendar Data

## 2. Agent Architecture

### 2.1 Base Agents

Each agent starts with basic functionality and is enhanced with additional capabilities:

1. **[Registration Agent](https://github.com/Taciturny/AI_University_Assistant/blob/main/src/assistant.py#L42)**
   - Course recommendations
   - Eligibility verification
   - Prerequisites checking
   - Section availability monitoring

2. **[Calendar Agent](https://github.com/Taciturny/AI_University_Assistant/blob/main/src/assistant.py#L129)**
   - Deadline tracking
   - Event management
   - Session-based filtering
   - Academic calendar maintenance

3. **[Student Query Agent](https://github.com/Taciturny/AI_University_Assistant/blob/main/src/assistant.py#L233)**
   - Grade calculation
   - Academic standing assessment
   - Course history tracking
   - Progress monitoring

### 2.2 Enhanced Capabilities
The enhanced prompt can be found [here](https://github.com/Taciturny/AI_University_Assistant/blob/main/docs/prompts/refined_prompts.json)
Enhanced agents incorporate:
- Content Awareness
- Personalization
- Proactive Guidance
- Multi-Factor Analysis


## 3. Implementation Details

### 3.1 Core Classes


#### UniversityAssistant Class
The `UniversityAssistant` class acts as the backbone of the system, handling core responsibilities such as:
- **Data Loading and Validation:** Ensures all inputs meet system requirements.
- **Agent Coordination:** Seamlessly integrates the functionality of the three specialized agents.
- **Error Handling:** Implements robust mechanisms for logging and recovering from system failures.

#### PromptManager Class
The `PromptManager` class optimizes interactions with the AI model by:
- Managing multiple prompt templates for varied use cases.
- Switching between base and refined prompts for improved contextual accuracy.
- Ensuring consistent updates with prompt versioning to align with system evolution.

### 3.2 Data Structures

The system utilizes structured JSON to represent and manage university data such as courses, sections, and instructors. Detailed JSON schema and examples can be found in the [data_gen.py](https://github.com/Taciturny/AI_University_Assistant/blob/main/data/data_gen.py) file.

#### Key Components of the Schema
- `courseId`: Unique identifier for the course.
- `courseName`: Name of the course.
- `department`: The department offering the course.
- `credits`: Number of credits assigned to the course.
- `prerequisites`: List of course IDs required as prerequisites.
- `availableSections`: Array of sections available for the course, including:
  - `sectionId`: Unique identifier for the section.
  - `instructor`: Name of the instructor.
  - `schedule`: Time and days the section is held.
  - `capacity`: Maximum number of students allowed in the section.
  - `enrolled`: Current number of enrolled students.

#### Usage
This JSON structure is used by:
- The **Registration Agent** to validate prerequisites and check section availability.
- The **Calendar Agent** to incorporate course schedules into the academic calendar.
- The **Student Query Agent** to retrieve course details, including instructor information and enrolled status.

## 4. Process Flows

### 4.1 Course Registration Flow

1. Student initiates registration request
2. System verifies student eligibility
3. Prerequisites are checked
4. Available sections are identified
5. Registration is confirmed or denied with reason

### 4.2 Calendar Event Processing

1. Event type is identified
2. Session filtering is applied
3. Relevant deadlines are extracted
4. Events are sorted by date
5. Filtered results are returned to student

## 5. Integration Points

### 5.1 External System Integration

The University Assistant was designed to support external API integrations, but due to time constraints, these features are currently placeholders. Below is an example structure to demonstrate potential integration with external systems.

```python
# Example API endpoint structure
@app.route('/api/v1/courses/recommend', methods=['POST'])
def recommend_courses():
    student_id = request.json.get('student_id')
    return jsonify(assistant.get_course_recommendations(student_id))
```

**Planned Features:**

Integration with university registration systems

Real-time course availability updates


### 5.2 Cohere AI Integration
Cohere's API is used for natural language processing tasks such as generating responses and recommendations. Here's an example of a Cohere API interaction:

```python
# Example Cohere API interaction
response = self.co.generate(
    prompt=prompt,
    max_tokens=100,
    temperature=0.7,
    k=0,
    stop_sequences=[],
    return_likelihoods='NONE'
)
```

## 6. Example Usage

### 6.1 Course Recommendation

```python
# Get course recommendations for a student
assistant = UniversityAssistant(api_key)
recommendations = assistant.get_course_recommendations("STU0001")
for course in recommendations:
    print(format_course_info(course))
```

### 6.2 Deadline Checking

```python
# Check upcoming deadlines for a session
deadlines = assistant.check_upcoming_deadlines("FULL_TERM")
for deadline in deadlines:
    print(format_deadline_info(deadline))
```

## 7. Testing Strategy

### 7.1 Unit Tests

- Test individual agent functions
- Validate data loading and processing
- Verify prompt generation and formatting
- Check error handling and recovery

### 7.2 Integration Tests

- Test agent interactions
- Verify data flow between components
- Validate end-to-end processes
- Check external API integration

## 8. Deployment Considerations

### 8.1 Requirements

- Python 3.10+
- Cohere API access
- JSON data storage
- Logging system

### 8.2 Configuration

- Environment variables for API keys
- Configurable data paths
- Adjustable logging levels
- Customizable prompt templates

## 9. Future Enhancements

1. Enhanced personalization using student history
2. Real-time course availability updates
3. Integration with university registration systems
4. Mobile application interface
5. Advanced analytics and reporting

## 10. Maintenance Guidelines

1. Regular prompt refinement and testing
2. Data validation and cleanup
3. Performance monitoring
4. Security updates and patches
5. User feedback integration
