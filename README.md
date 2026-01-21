# Health Resource Allocator

A comprehensive FastAPI-based system that transforms health recommendations from Elyx's HealthSpan AI into personalized, scheduled tasks with intelligent resource coordination.

## 🎯 Assignment Overview

This project implements a **Resource Allocator** that:
- Takes an action plan of health activities ordered by priority
- Transforms them into daily, weekly, monthly, or yearly scheduled tasks
- Coordinates with AI agents, humans, and resources based on availability
- Handles all constraints including travel, equipment, and specialist schedules


## Assignment Requirements Met

### 1. **Data Generation** (Requirement: 100+ activities, 3 months availability)
-  **100+ realistic health activities** across all required types
-  **21 resources** with 3-month availability schedules  
-  **Comprehensive client constraints** including travel and work schedules

### 2. **Activity Types** (Requirement: All 5 types covered)
-  **Fitness**: 25 activities (running, yoga, swimming, HIIT, etc.)
-  **Food**: 30 activities (Mediterranean meals, smoothies, supplements)
-  **Medication**: 25 activities (vitamins, probiotics, health supplements)
-  **Therapy**: 20 activities (sauna, massage, acupuncture, red light therapy)
-  **Consultation**: 20 activities (specialist appointments, health coaching)

### 3. **Activity Properties** (Requirement: 10 specific fields)
Each activity includes all required fields:
1. **Activity Type** - One of the 5 categories
2. **Frequency** - "3 times a week", "daily", "monthly", etc.
3. **Details** - Specific instructions (e.g., "Maintain HR between 120-140")
4. **Facilitator** - Who conducts it (trainer, self, specialist)
5. **Location** - Where it takes place
6. **Remote Capability** - Can it be done via video call
7. **Prep Requirements** - What needs to be prepared beforehand
8. **Backup Activities** - Alternative options if primary unavailable
9. **Skip Adjustments** - What to do if activity is missed
10. **Metrics** - What data to collect from the activity

### 4. **Resource Coordination** (Assignment Core Requirement)
-  **Equipment Management** - Gym access, pools, sauna availability
-  **Specialist Scheduling** - Doctor, trainer, therapist calendars
-  **Allied Health** - Physiotherapists, dietitians, occupational therapists
-  **Capacity Management** - Prevents double-booking, respects limits

### 5. **Constraint Handling** (Assignment Core Requirement)
-  **Travel Plans** - No scheduling during client travel
-  **Client Schedule** - Respects work hours (9-5 weekdays)
-  **Equipment Availability** - Matches activities to available equipment
-  **Specialist Availability** - Coordinates with professional schedules

### 6. **Calendar Output** (Assignment Requirement)
-  **Readable Format** - HTML and text calendar views
-  **Resource Information** - Shows assigned equipment and specialists
-  **Daily Summaries** - Time commitments and activity counts
-  **Conflict Resolution** - Handles and reports scheduling conflicts

## 🚀 Quick Start

### Installation
```bash
git clone [repository-url]
cd health_resource_allocator
pip install -r requirements.txt
```

### Run Locally
```bash
python main.py
# or
uvicorn main:app --reload
```

Visit `http://localhost:8000` to see the web interface.

### Generate Your First Schedule
```bash
# Via web interface
curl -X POST "http://localhost:8000/generate-schedule?weeks=12"

# Via browser
http://localhost:8000/generate-schedule
```

## 📡 API Endpoints

### Core Scheduling Endpoints
- `POST /generate-schedule` - **Create personalized schedule** (main assignment function)
- `GET /calendar` - **View schedule in HTML calendar** (assignment output requirement)
- `GET /activities` - List all 100+ health activities with filtering
- `GET /resources` - Get equipment and specialist availability

### Data Endpoints (Assignment Requirements)
- `GET /data/activities.json` - **Raw activity data** (100+ activities requirement)
- `GET /data/resources.json` - **Resource availability data** (3 months requirement)  
- `GET /data/client_schedule.json` - **Client constraints data**
- `GET /data/current_schedule.json` - **Generated schedule export**

### Analysis Endpoints
- `GET /stats` - Comprehensive system statistics
- `GET /validate-schedule` - Check for scheduling conflicts
- `GET /health` - System health and data status

## 📊 Sample Usage

### 1. Generate Schedule
```http
POST /generate-schedule
{
  "start_date": "2024-01-01",
  "weeks": 12
}
```

**Response:**
```json
{
  "message": "Schedule generated successfully! 87 activities scheduled across 45 days.",
  "total_scheduled_activities": 87,
  "activities_by_type": {
    "fitness": 18,
    "food": 25,
    "medication": 21,
    "therapy": 12,
    "consultation": 11
  }
}
```

### 2. View Calendar
Visit `/calendar` for formatted schedule:
```
📅 Monday, January 01, 2024
    3 activities • 1h 30m
────────────────────────────────────
  06:30-07:00  │ 💪 🔥 Morning Run
               │ 📍 Park • ⏱️ 30min
  
  07:15-07:20  │ 💊 Vitamin D3 Supplement  
               │ 📍 Home • ⏱️ 5min
  
  18:30-19:00  │ 🥗 Mediterranean Dinner
               │ 📍 Home • ⏱️ 30min
               │ 🔧 Nutritionist consultation
```

## 🔧 System Features

### Intelligent Scheduling
- **Priority-based**: Higher priority activities get preferred time slots
- **Frequency parsing**: Handles "3 times a week", "daily", "bi-weekly", etc.
- **Conflict resolution**: Automatic rescheduling and buffer time management
- **Realistic limits**: Prevents over-scheduling (max 4 activities/day weekdays)

### Resource Management  
- **Equipment booking**: Prevents double-booking of gym, pool, sauna
- **Specialist coordination**: Matches activities with available professionals
- **Capacity tracking**: Respects resource limits and availability windows
- **Backup planning**: Alternative resources when primary unavailable

### Constraint Handling
- **Travel awareness**: No activities during client travel dates
- **Work schedule**: Avoids 9-5 weekday conflicts
- **Preference optimization**: Prioritizes client's preferred time slots
- **Buffer management**: 10-15 minute gaps between activities

## 📁 Project Structure

```
health_resource_allocator/
├── main.py                 # FastAPI application and endpoints
├── models.py              # Pydantic data models
├── scheduler.py           # Core scheduling algorithm  
├── data_generator.py      # Sample data generation
├── requirements.txt       # Dependencies
├── Procfile              # Deployment configuration
├── README.md             # This file
└── data/                 # Generated data files
    ├── activities.json    # 120+ health activities
    ├── resources.json     # Resource availability (3 months)
    ├── client_schedule.json # Client constraints
    └── scheduled_activities.json # Generated schedules
```

## 🎯 Key Assignment Components

### Data Models (models.py)
- `Activity` - Represents health activities with all 10 required fields
- `ResourceAvailability` - Equipment and specialist schedules
- `ClientSchedule` - Travel, work, and preference constraints
- `ScheduledActivity` - Final scheduled items with resource assignments

### Scheduling Algorithm (scheduler.py)
- Frequency parsing for realistic scheduling patterns
- Resource matching and availability checking  
- Conflict detection and resolution
- Priority-based time slot allocation

### Data Generation (data_generator.py)
- 120+ realistic health activities across 5 types
- 3 months of resource availability data
- Realistic client constraints and travel schedules

## 🌐 Deployment

### Render.com (Recommended)
```bash
# Automatic deployment via GitHub
# Uses Procfile: web: uvicorn main:app --host=0.0.0.0 --port=$PORT
```

### Local Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performance & Scalability

- **Data Volume**: Handles 100+ activities, 21 resources efficiently
- **Scheduling Speed**: Generates 12-week schedules in <2 seconds
- **Memory Usage**: ~50MB for full dataset and schedule generation
- **API Response**: Most endpoints respond in <100ms

## 🔍 Testing & Validation

### Automated Validation
- Schedule conflict detection (overlapping activities)
- Resource availability verification
- Frequency compliance checking
- Client constraint validation

### Manual Testing
```bash
# Test schedule generation
curl -X POST "http://localhost:8000/generate-schedule?weeks=4"

# Validate results
curl "http://localhost:8000/validate-schedule"

# Check specific data
curl "http://localhost:8000/activities?activity_type=fitness&priority_max=5"
```

## 🤖 AI & GenAI Usage

### Code Generation Prompts:
1. "Create a Python FastAPI project structure for a health resource allocator that transforms health recommendations into scheduled tasks with resource coordination"

2. "Generate realistic sample data for 100+ health activities covering fitness, food, medication, therapy, and consultation categories with all required fields"

3. "Create a scheduling algorithm that parses frequency strings like '3 times a week' and coordinates with resource availability while respecting client constraints"

4. "Design FastAPI endpoints for the health resource allocator including calendar views, data exports, and schedule generation with proper error handling"

5. "Help me deploy this FastAPI application to Render.com with proper configuration for a health scheduling system"

### AI-Generated Components:
- **Data models** with Pydantic validation
- **Sample data generation** for realistic health activities  
- **Scheduling algorithm** with frequency parsing
- **API endpoints** with comprehensive documentation
- **HTML calendar views** with styling and formatting
- **Deployment configuration** for cloud platforms

### Human Oversight:
- 🔍 **Algorithm logic review** and optimization
- 🔍 **Data validation** and realism checks
- 🔍 **API design** and endpoint structure  
- 🔍 **Assignment compliance** verification
- 🔍 **Documentation** accuracy and completeness


## 💡 Assumptions & Design Decisions

#### Activity Prioritization
- **Priority Scale**: 1-10 where 1 = highest priority (most critical for health)
- **Priority Impact**: Activities with priority 1-3 get first choice of preferred time slots
- **Health Criticality**: Medication and consultation activities typically have higher priorities (1-5)
- **Lifestyle Activities**: Fitness and food activities typically have medium priorities (3-7)
- **Wellness Activities**: Therapy activities typically have lower priorities (5-8)

#### Duration Assumptions
- **Medication Activities**: 5 minutes (realistic for taking pills/supplements)
- **Food Preparation**: 15-30 minutes depending on complexity
- **Fitness Activities**: 30-60 minutes (capped at 90 minutes to prevent exhaustion)
- **Therapy Sessions**: 45-60 minutes (standard professional session length)
- **Consultations**: 45-60 minutes (typical appointment duration)
- **Eye Exercises**: 15 minutes (as specified in assignment examples)

#### Frequency Interpretation Philosophy
- **"Daily" Activities**: Scheduled once per day to avoid overwhelming schedules
- **"3 times daily"**: Interpreted as "daily with meal integration" (one consolidated activity)
- **"Twice daily"**: Simplified to once daily with morning/evening preference
- **"3 times a week"**: Distributed as Monday/Wednesday/Friday pattern
- **"Every other day"**: Interpreted as 3-4 times per week
- **"With meals"**: Scheduled around typical meal times (breakfast, lunch, dinner)

### 🗓️ Scheduling Philosophy Assumptions

#### Time Management
- **Daily Activity Limits**: 
  - Weekdays: Maximum 4 activities (realistic for working people)
  - Weekends: Maximum 5 activities (more flexibility)
- **Time Commitment Limits**:
  - Weekdays: Maximum 3 hours total (180 minutes)
  - Weekends: Maximum 4 hours total (240 minutes)
- **Buffer Time**: 10-15 minutes between activities for transitions/preparation
- **Realistic Gaps**: No back-to-back scheduling to allow for real-world delays

#### Work-Life Balance
- **Work Hours**: 9 AM - 5 PM weekdays are protected (no personal health activities)
- **Available Windows**: 
  - Morning: 6:30 AM - 8:30 AM
  - Evening: 6:30 PM - 8:30 PM
  - Weekends: 8:00 AM - 7:00 PM (more flexible)
- **Travel Impact**: Complete blackout during travel dates (no activities scheduled)

#### Activity Distribution
- **Weekly Spread**: Activities distributed evenly across the week when possible
- **Type Preferences**: Different activity types prefer different days:
  - Fitness: Monday/Wednesday/Friday (classic workout schedule)
  - Consultations: Tuesday/Thursday (when professionals are typically available)
  - Therapy: Saturday (when many wellness centers operate)
  - Food/Medication: Any day (flexible scheduling)

### 🔧 Resource Management Assumptions

#### Equipment Availability
- **Gym Equipment**: High capacity (20-50 people) during operating hours
- **Specialized Equipment**: Lower capacity (sauna: 8 people, massage tables: 4)
- **Operating Hours**: Equipment generally available 6 AM - 10 PM
- **Maintenance Windows**: 15% of dates unavailable for maintenance/cleaning
- **Booking Logic**: First-come, first-served within capacity limits

#### Professional Availability
- **Specialists**: Work standard business hours (9 AM - 5 PM) weekdays
- **Allied Health**: More flexible hours (8 AM - 6 PM) including some Saturdays
- **Capacity**: One client at a time for personalized services
- **Availability Rate**: 70-85% of business days (accounting for vacations, sick days)
- **Booking Prevention**: Hard conflicts prevented (no double-booking)

#### Resource Matching Logic
- **Keyword Matching**: Simple but effective (e.g., "swimming" activity → pool resource)
- **Fallback Options**: If specific resource unavailable, activity can often proceed without it
- **Self-Directed Activities**: Many activities (medication, some fitness) don't require special resources
- **Professional Matching**: Activities requiring facilitators matched to available specialists

### 👤 Client Constraint Assumptions

#### Travel and Availability
- **Travel Dates**: Complete unavailability (no activities scheduled)
- **Work Schedule**: Traditional 9-5 Monday-Friday (can be customized)
- **Blackout Dates**: Personal days off from health activities (sick days, family events)
- **Preferred Times**: Client has 3 preferred time windows they favor

#### Behavioral Assumptions
- **Adherence**: Client will follow scheduled activities as planned
- **Flexibility**: Client can handle 10-15 minute scheduling windows
- **Preparation**: Client can do required prep work before activities
- **Travel Time**: Client can travel between locations within buffer time

### 📊 Data Generation Assumptions

#### Activity Realism
- **Evidence-Based**: All activities based on real health recommendations
- **Variety**: 120 activities provide enough variety for 12+ weeks without repetition
- **Seasonal Independence**: Activities not tied to seasons (can be scheduled year-round)
- **Location Flexibility**: Most activities can be done in multiple locations

#### Resource Reality
- **Business Operations**: Resources follow typical business operational patterns
- **Capacity Modeling**: Based on real-world capacity of gyms, clinics, wellness centers
- **Availability Patterns**: Account for weekends, holidays, maintenance schedules
- **Geographic Assumptions**: All resources assumed within reasonable travel distance

### 🤖 Technical Implementation Assumptions

#### System Performance
- **Response Time**: API endpoints should respond within 2 seconds
- **Memory Usage**: System should handle full dataset in under 100MB RAM
- **Concurrency**: Single-user system (not designed for multi-user concurrent scheduling)
- **Data Persistence**: JSON files sufficient for demonstration (easily upgraded to database)

#### Error Handling Philosophy
- **Graceful Degradation**: If resources unavailable, schedule activity without special resources
- **Conflict Resolution**: Try alternative times before marking activity as unscheduled
- **User Feedback**: Always provide clear messages about why scheduling failed
- **Recovery Options**: Suggest alternatives or backup activities when primary fails

#### API Design Assumptions
- **RESTful Design**: Standard REST conventions for predictable API behavior
- **JSON Format**: All data exchange in JSON for universal compatibility
- **Browser Friendly**: GET endpoints available for easy browser testing
- **Documentation**: Swagger/OpenAPI for comprehensive API documentation

### 🎯 Assignment-Specific Assumptions

#### Scope Limitations
- **Single Client**: System designed for one client at a time
- **12-Week Window**: Optimal scheduling period for meaningful health planning
- **English Language**: All activities and descriptions in English
- **Metric System**: Time in minutes, no unit conversions needed

#### Real-World Practicality
- **Adherence Expectations**: 70-80% schedule adherence considered successful
- **Backup Activity Usage**: 10-20% of activities may need backup alternatives
- **Scheduling Conflicts**: Some conflicts expected and acceptable (documented)
- **Resource Unavailability**: 15-30% resource conflicts expected in real world

#### Health and Safety
- **Medical Supervision**: Assume activities are pre-approved by healthcare providers
- **Physical Limitations**: No assessment of client physical capabilities
- **Medication Interactions**: No checking for drug interactions or contraindications
- **Emergency Protocols**: No emergency or urgent care scheduling

### 🔄 Future Enhancement Assumptions

#### Scalability Considerations
- **Database Migration**: JSON files designed to easily migrate to PostgreSQL/MongoDB
- **Multi-User Support**: Current single-user design can be extended
- **Mobile Integration**: API designed to support future mobile applications
- **Real-Time Updates**: Architecture supports real-time resource availability updates

#### AI Integration Potential
- **Learning Patterns**: System could learn from user preferences and adherence
- **Smart Recommendations**: Could suggest optimal scheduling based on historical data
- **Predictive Conflicts**: Could predict and prevent scheduling conflicts
- **Health Outcome Correlation**: Could track activity effectiveness over time

---


## 📞 Support & Documentation

- **API Documentation**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **Health Check**: `/health`
- **System Stats**: `/stats`

---


