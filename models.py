from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime, date, time
from enum import Enum
import json

class ActivityType(str, Enum):
    FITNESS = "fitness"
    FOOD = "food"
    MEDICATION = "medication"
    THERAPY = "therapy"
    CONSULTATION = "consultation"

class Activity(BaseModel):
    id: int
    activity_type: ActivityType
    name: str
    priority: int = Field(ge=1, le=10, description="1 = highest priority, 10 = lowest")
    frequency: str
    details: str
    facilitator: Optional[str] = None
    location: str
    remote_capable: bool = False
    prep_required: str = ""
    backup_activities: List[str] = []
    skip_adjustments: str = ""
    metrics: List[str] = []
    duration_minutes: int = Field(default=60, ge=1, le=480)

    @validator('frequency')
    # def validate_frequency(cls, v):
    #     valid_patterns = ['daily', 'weekly', 'monthly', 'yearly', 'times', 'twice']
    #     if not any(pattern in v.lower() for pattern in valid_patterns):
    #         raise ValueError('Frequency must contain valid time patterns')
    #     return v
    
    def validate_frequency(cls, v):
        """More flexible frequency validation"""
        v_lower = v.lower()
        valid_patterns = [
            'daily', 'weekly', 'monthly', 'yearly', 
            'times', 'twice', 'every', 'per', 
            'meal', 'day', 'week', 'month', 'year',
            'other', 'bi-', 'tri-', 'quad-'
        ]
        
        if any(pattern in v_lower for pattern in valid_patterns):
            return v
        
        # If no valid pattern found, still allow it but warn
        print(f"Warning: Unusual frequency pattern '{v}' - allowing anyway")
        return v

class ResourceAvailability(BaseModel):
    resource_type: Literal["equipment", "specialist", "allied_health"]
    resource_id: str
    name: str
    available_dates: List[date]
    available_times: List[str]
    capacity: int = Field(default=1, ge=1)

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class ClientSchedule(BaseModel):
    client_id: str = "client_001"
    busy_periods: List[Dict[str, Any]] = []
    travel_dates: List[date] = []
    preferred_times: List[str] = ["06:00-08:00", "12:00-13:00", "18:00-20:00"]
    blackout_dates: List[date] = []

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class ScheduledActivity(BaseModel):
    activity: Activity
    scheduled_date: date
    scheduled_time: str
    duration_minutes: int
    resources_assigned: List[str] = []
    location: str
    notes: str = ""
    status: str = "scheduled"

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class ScheduleResponse(BaseModel):
    message: str
    start_date: str
    end_date: str
    total_scheduled_activities: int
    activities_by_type: Dict[str, int]
    scheduling_conflicts: List[str] = []
    unscheduled_activities: List[str] = []