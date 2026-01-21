from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date, datetime, timedelta
from collections import defaultdict
import json
import os
import traceback
import uvicorn

from models import Activity, ScheduledActivity, ResourceAvailability, ClientSchedule, ScheduleResponse
from scheduler import ResourceAllocatorScheduler
from data_generator import DataGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Health Resource Allocator API",
    description="Transform health recommendations into personalized, scheduled tasks with resource coordination",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scheduler instance
scheduler = ResourceAllocatorScheduler()
data_initialized = False

def initialize_data():
    """Initialize or regenerate sample data"""
    global data_initialized
    
    try:
        os.makedirs('data', exist_ok=True)
        
        # Always regenerate data for fresh demo
        print("🔄 Generating fresh sample data...")
        generator = DataGenerator()
        generator.save_data_to_files()
        
        # Load data into scheduler
        print("📊 Loading data into scheduler...")
        scheduler.load_data()
        
        data_initialized = True
        print("✅ Data initialization complete")
        
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
        print(traceback.format_exc())
        raise

@app.on_event("startup")
async def startup_event():
    """Initialize everything on startup"""
    initialize_data()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Enhanced welcome page with full API documentation"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Health Resource Allocator</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; 
                   margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; 
                        padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; margin-bottom: 10px; font-size: 2.5em; }
            .subtitle { color: #7f8c8d; font-size: 1.2em; margin-bottom: 30px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 20px; margin: 30px 0; }
            .stat-card { background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; 
                        border-left: 4px solid #3498db; }
            .stat-number { font-size: 2em; font-weight: bold; color: #2c3e50; }
            .stat-label { color: #7f8c8d; margin-top: 5px; }
            .endpoints { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .endpoint { background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #27ae60; }
            .endpoint h3 { margin: 0 0 10px 0; color: #2c3e50; }
            .endpoint p { color: #7f8c8d; margin: 5px 0; }
            .method { display: inline-block; padding: 4px 8px; border-radius: 4px; color: white; 
                     font-size: 0.8em; font-weight: bold; }
            .get { background: #27ae60; }
            .post { background: #3498db; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 12px 24px; 
                  text-decoration: none; border-radius: 6px; margin: 10px 10px 10px 0; }
            .btn:hover { background: #2980b9; }
            .btn-success { background: #27ae60; }
            .btn-success:hover { background: #229954; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Health Resource Allocator</h1>
            <p class="subtitle">Transform health recommendations into personalized, scheduled tasks with intelligent resource coordination</p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">100+</div>
                    <div class="stat-label">Health Activities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">21</div>
                    <div class="stat-label">Resource Types</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">12</div>
                    <div class="stat-label">Weeks Scheduling</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Activity Categories</div>
                </div>
            </div>

            <h2>🚀 Quick Actions</h2>
            <a href="/generate-schedule" class="btn btn-success">Generate Schedule</a>
            <a href="/calendar" class="btn">View Calendar</a>
            <a href="/docs" class="btn">API Documentation</a>
            <a href="/stats" class="btn">View Statistics</a>

            <h2>📡 API Endpoints</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <h3><span class="method get">GET</span> /activities</h3>
                    <p>Retrieve all health activities with optional filtering by type and priority</p>
                    <p><strong>Parameters:</strong> activity_type, priority_max</p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method get">GET</span> /resources</h3>
                    <p>Get availability data for equipment, specialists, and allied health professionals</p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method post">POST</span> /generate-schedule</h3>
                    <p>Create a personalized schedule based on priorities and constraints</p>
                    <p><strong>Parameters:</strong> start_date (optional), weeks (default: 12)</p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method get">GET</span> /calendar</h3>
                    <p>View the generated schedule in a beautiful HTML calendar format</p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method get">GET</span> /stats</h3>
                    <p>Get comprehensive statistics about activities, resources, and scheduling</p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method get">GET</span> /health</h3>
                    <p>System health check and status information</p>
                </div>
            </div>

            <h2>🏗️ System Features</h2>
            <ul>
                <li><strong>Intelligent Scheduling:</strong> Prioritizes activities and handles resource conflicts</li>
                <li><strong>Resource Coordination:</strong> Manages equipment, specialists, and allied health availability</li>
                <li><strong>Constraint Handling:</strong> Respects client travel, work schedules, and preferences</li>
                <li><strong>Comprehensive Data:</strong> 100+ realistic health activities across 5 categories</li>
                <li><strong>Flexible Frequencies:</strong> Supports daily, weekly, monthly scheduling patterns</li>
                <li><strong>Backup Planning:</strong> Provides alternatives for missed or conflicted activities</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/activities", response_model=List[Activity])
async def get_activities(
    activity_type: Optional[str] = Query(None, description="Filter by activity type (fitness, food, medication, therapy, consultation)"),
    priority_max: Optional[int] = Query(None, description="Filter by maximum priority level (1-10)"),
    limit: Optional[int] = Query(None, description="Limit number of results")
):
    """Get activities with enhanced filtering options"""
    try:
        activities = scheduler.activities.copy()
        
        if activity_type:
            activities = [a for a in activities if a.activity_type.value == activity_type.lower()]
        
        if priority_max:
            activities = [a for a in activities if a.priority <= priority_max]
        
        if limit:
            activities = activities[:limit]
        
        return activities
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving activities: {str(e)}")

@app.get("/resources")
async def get_resources():
    """Get detailed resource availability information"""
    try:
        resources_summary = []
        
        for resource in scheduler.resources:
            summary = {
                "resource_type": resource.resource_type,
                "resource_id": resource.resource_id,
                "name": resource.name,
                "capacity": resource.capacity,
                "available_dates_count": len(resource.available_dates),
                "available_times": resource.available_times,
                "availability_percentage": len(resource.available_dates) / 90 * 100,  # 90 days = 3 months
                "next_available": min(resource.available_dates).isoformat() if resource.available_dates else None
            }
            resources_summary.append(summary)
        
        # Group by type for better organization
        grouped = {"equipment": [], "specialist": [], "allied_health": []}
        for resource in resources_summary:
            grouped[resource["resource_type"]].append(resource)
        
        return {
            "total_resources": len(resources_summary),
            "by_type": grouped,
            "summary": {
                "equipment": len(grouped["equipment"]),
                "specialists": len(grouped["specialist"]),
                "allied_health": len(grouped["allied_health"])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resources: {str(e)}")

@app.get("/client-schedule")
async def get_client_schedule():
    """Get client schedule constraints and preferences"""
    try:
        if not scheduler.client_schedule:
            raise HTTPException(status_code=404, detail="Client schedule not found")
        
        return {
            "client_id": scheduler.client_schedule.client_id,
            "constraints": {
                "busy_periods": len(scheduler.client_schedule.busy_periods),
                "travel_dates": len(scheduler.client_schedule.travel_dates),
                "blackout_dates": len(getattr(scheduler.client_schedule, 'blackout_dates', []))
            },
            "preferences": {
                "preferred_times": scheduler.client_schedule.preferred_times
            },
            "upcoming": {
                "next_travel": min(scheduler.client_schedule.travel_dates).isoformat() if scheduler.client_schedule.travel_dates else None,
                "travel_days_remaining": len([d for d in scheduler.client_schedule.travel_dates if d >= date.today()])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving client schedule: {str(e)}")

# @app.post("/generate-schedule", response_model=ScheduleResponse)
# async def generate_schedule(
#     background_tasks: BackgroundTasks,
#     start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD), defaults to today"),
#     weeks: Optional[int] = Query(12, description="Number of weeks to schedule (1-24)", ge=1, le=24)
# ):
#     """Generate personalized schedule with comprehensive response"""
#     try:
#         # Parse start date
#         if start_date:
#             try:
#                 start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
#             except ValueError:
#                 raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
#         else:
#             start_date_obj = date.today()
        
#         # Generate schedule
#         print(f"🗓️  Generating schedule from {start_date_obj} for {weeks} weeks...")
#         scheduled_activities = scheduler.create_schedule(start_date_obj, weeks)
        
#         # Export in background
#         background_tasks.add_task(scheduler.export_to_json, "current_schedule.json")
        
#         # Calculate statistics
#         activities_by_type = {}
#         for activity_type in ["fitness", "food", "medication", "therapy", "consultation"]:
#             count = len([s for s in scheduled_activities if s.activity.activity_type == activity_type])
#             activities_by_type[activity_type] = count
        
#         response = ScheduleResponse(
#             message=f"Schedule generated successfully for {len(scheduled_activities)} activities",
#             start_date=start_date_obj.isoformat(),
#             end_date=(start_date_obj + timedelta(weeks=weeks)).isoformat(),
#             total_scheduled_activities=len(scheduled_activities),
#             activities_by_type=activities_by_type,
#             scheduling_conflicts=scheduler.scheduling_conflicts,
#             unscheduled_activities=scheduler.unscheduled_activities
#         )
        
#         return response
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"❌ Error generating schedule: {e}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"Error generating schedule: {str(e)}")


# @app.get("/generate-schedule")
# async def generate_schedule_get(
#     start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD), defaults to today"),
#     weeks: Optional[int] = Query(12, description="Number of weeks to schedule (1-24)", ge=1, le=24)
# ):
#     """Generate schedule via GET request (browser-friendly)"""
#     try:
#         # Parse start date
#         if start_date:
#             try:
#                 start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
#             except ValueError:
#                 raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
#         else:
#             start_date_obj = date.today()
        
#         # Generate schedule
#         print(f"🗓️  Generating schedule from {start_date_obj} for {weeks} weeks...")
#         scheduled_activities = scheduler.create_schedule(start_date_obj, weeks)
        
#         # Export schedule
#         scheduler.export_to_json("current_schedule.json")
        
#         # Calculate statistics
#         activities_by_type = {}
#         for activity_type in ["fitness", "food", "medication", "therapy", "consultation"]:
#             count = len([s for s in scheduled_activities if s.activity.activity_type == activity_type])
#             activities_by_type[activity_type] = count
        
#         response_data = {
#             "message": f"✅ Schedule generated successfully!",
#             "summary": {
#                 "start_date": start_date_obj.isoformat(),
#                 "end_date": (start_date_obj + timedelta(weeks=weeks)).isoformat(),
#                 "total_scheduled_activities": len(scheduled_activities),
#                 "activities_by_type": activities_by_type,
#                 "scheduling_conflicts": len(scheduler.scheduling_conflicts),
#                 "unscheduled_activities": len(scheduler.unscheduled_activities)
#             },
#             "next_steps": [
#                 "View your calendar at /calendar",
#                 "Get detailed stats at /stats", 
#                 "Download JSON data from /data/current_schedule.json"
#             ]
#         }
        
#         return response_data
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"❌ Error generating schedule: {e}")
#         raise HTTPException(status_code=500, detail=f"Error generating schedule: {str(e)}")


@app.post("/generate-schedule", response_model=ScheduleResponse)
async def generate_schedule(
    background_tasks: BackgroundTasks,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD), defaults to today"),
    weeks: Optional[int] = Query(12, description="Number of weeks to schedule (1-24)", ge=1, le=24)
):
    """Generate personalized schedule with comprehensive response"""
    try:
        # Parse start date
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        else:
            start_date_obj = date.today()
        
        # Clear any existing schedule
        scheduler.scheduled_activities = []
        scheduler.daily_schedules = defaultdict(list)
        
        # Generate schedule
        print(f"🗓️  Generating schedule from {start_date_obj} for {weeks} weeks...")
        scheduled_activities = scheduler.create_schedule(start_date_obj, weeks)
        
        # Export in background
        background_tasks.add_task(scheduler.export_to_json, "current_schedule.json")
        
        # Calculate statistics
        activities_by_type = {}
        for activity_type in ["fitness", "food", "medication", "therapy", "consultation"]:
            count = len([s for s in scheduled_activities if s.activity.activity_type == activity_type])
            activities_by_type[activity_type] = count
        
        response = ScheduleResponse(
            message=f"Schedule generated successfully! {len(scheduled_activities)} activities scheduled across {len(scheduler.daily_schedules)} days.",
            start_date=start_date_obj.isoformat(),
            end_date=(start_date_obj + timedelta(weeks=weeks)).isoformat(),
            total_scheduled_activities=len(scheduled_activities),
            activities_by_type=activities_by_type,
            scheduling_conflicts=scheduler.scheduling_conflicts[:10],  # First 10 conflicts
            unscheduled_activities=scheduler.unscheduled_activities[:10]  # First 10 unscheduled
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating schedule: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating schedule: {str(e)}")

@app.get("/generate-schedule")
async def generate_schedule_get(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD), defaults to today"),
    weeks: Optional[int] = Query(12, description="Number of weeks to schedule (1-24)", ge=1, le=24)
):
    """Generate schedule via GET request (browser-friendly)"""
    try:
        # Parse start date
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        else:
            start_date_obj = date.today()
        
        # Clear any existing schedule
        scheduler.scheduled_activities = []
        scheduler.daily_schedules = defaultdict(list)
        
        # Generate schedule
        print(f"🗓️  Generating schedule from {start_date_obj} for {weeks} weeks...")
        scheduled_activities = scheduler.create_schedule(start_date_obj, weeks)
        
        # Export schedule
        scheduler.export_to_json("current_schedule.json")
        
        # Calculate statistics
        activities_by_type = {}
        for activity_type in ["fitness", "food", "medication", "therapy", "consultation"]:
            count = len([s for s in scheduled_activities if s.activity.activity_type == activity_type])
            activities_by_type[activity_type] = count
        
        # Create daily summaries
        daily_summaries = []
        activities_by_date = defaultdict(list)
        
        for activity in scheduled_activities:
            activities_by_date[activity.scheduled_date].append(activity)
        
        for schedule_date in sorted(activities_by_date.keys())[:10]:  # First 10 days
            daily_activities = activities_by_date[schedule_date]
            total_duration = sum(a.duration_minutes for a in daily_activities)
            
            daily_summaries.append({
                "date": schedule_date.strftime("%A, %B %d, %Y"),
                "activities": len(daily_activities),
                "duration": f"{total_duration//60}h {total_duration%60}m"
            })
        
        return {
            "status": "✅ Success",
            "message": f"Generated realistic schedule with {len(scheduled_activities)} activities",
            "summary": {
                "start_date": start_date_obj.isoformat(),
                "end_date": (start_date_obj + timedelta(weeks=weeks)).isoformat(),
                "total_scheduled_activities": len(scheduled_activities),
                "activities_by_type": activities_by_type,
                "days_with_activities": len(activities_by_date),
                "conflicts": len(scheduler.scheduling_conflicts),
                "unscheduled": len(scheduler.unscheduled_activities)
            },
            "daily_summaries": daily_summaries,
            "next_steps": [
                "📅 View calendar at /calendar",
                "📊 Get stats at /stats",
                "📁 Download JSON at /data/current_schedule.json"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating schedule: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating schedule: {str(e)}")

# Add a new endpoint to check for schedule conflicts
@app.get("/validate-schedule")
async def validate_current_schedule():
    """Validate current schedule for conflicts"""
    if not scheduler.scheduled_activities:
        return {"message": "No schedule to validate. Generate a schedule first."}
    
    conflicts = []
    activities_by_date = defaultdict(list)
    
    for activity in scheduler.scheduled_activities:
        activities_by_date[activity.scheduled_date.isoformat()].append(activity)
    
    for date_str, daily_activities in activities_by_date.items():
        sorted_activities = sorted(daily_activities, 
                                 key=lambda x: scheduler.time_to_minutes(x.scheduled_time.split('-')[0]))
        
        for i in range(len(sorted_activities) - 1):
            current = sorted_activities[i]
            next_activity = sorted_activities[i + 1]
            
            current_end = scheduler.time_to_minutes(current.scheduled_time.split('-')[1])
            next_start = scheduler.time_to_minutes(next_activity.scheduled_time.split('-')[0])
            
            if current_end > next_start:
                conflicts.append({
                    "date": date_str,
                    "conflict": f"{current.activity.name} ({current.scheduled_time}) overlaps {next_activity.activity.name} ({next_activity.scheduled_time})",
                    "overlap_minutes": current_end - next_start
                })
    
    return {
        "total_activities": len(scheduler.scheduled_activities),
        "conflicts_found": len(conflicts),
        "conflicts": conflicts,
        "status": "✅ Valid" if len(conflicts) == 0 else f"⚠️ {len(conflicts)} conflicts found"
    }


@app.get("/calendar", response_class=HTMLResponse)
async def get_calendar_view():
    """Enhanced HTML calendar view"""
    try:
        if not scheduler.scheduled_activities:
            # Auto-generate schedule
            await generate_schedule(BackgroundTasks())
        
        calendar_text = scheduler.generate_calendar_output()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Health Schedule Calendar</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                }}
                .calendar-container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .calendar-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .calendar-header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}
                .calendar-content {{
                    padding: 30px;
                    white-space: pre-line;
                    line-height: 1.6;
                    font-size: 14px;
                }}
                .actions {{
                    text-align: center;
                    padding: 20px;
                    border-top: 1px solid #eee;
                    background: #f8f9fa;
                }}
                .btn {{
                    display: inline-block;
                    background: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 0 10px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                }}
                .btn:hover {{ background: #2980b9; }}
                .btn-secondary {{ background: #95a5a6; }}
                .btn-secondary:hover {{ background: #7f8c8d; }}
                @media (max-width: 768px) {{
                    body {{ padding: 10px; }}
                    .calendar-header {{ padding: 20px; }}
                    .calendar-header h1 {{ font-size: 2em; }}
                    .calendar-content {{ padding: 20px; font-size: 12px; }}
                }}
            </style>
        </head>
        <body>
            <div class="calendar-container">
                <div class="calendar-header">
                    <h1>🗓️ Your Personalized Health Schedule</h1>
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                <div class="calendar-content">{calendar_text.replace('<', '&lt;').replace('>', '&gt;')}</div>
                <div class="actions">
                    <a href="/calendar/text" class="btn">Text Format</a>
                    <a href="/generate-schedule" class="btn">Regenerate</a>
                    <a href="/" class="btn btn-secondary">Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        error_html = f"""
        <html><body style="font-family: Arial; padding: 20px;">
        <h2>❌ Calendar Error</h2>
        <p>Sorry, there was an error generating your calendar: {str(e)}</p>
        <a href="/generate-schedule" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Generate Schedule First</a>
        </body></html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/calendar/text")
async def get_calendar_text():
    """Get calendar as JSON for API consumption"""
    try:
        if not scheduler.scheduled_activities:
            return {"message": "No schedule available. Generate one first.", "calendar": ""}
        
        return {
            "calendar": scheduler.generate_calendar_output(),
            "metadata": {
                "total_activities": len(scheduler.scheduled_activities),
                "date_range": {
                    "start": min(a.scheduled_date for a in scheduler.scheduled_activities).isoformat(),
                    "end": max(a.scheduled_date for a in scheduler.scheduled_activities).isoformat()
                },
                "generated_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating calendar text: {str(e)}")

@app.get("/stats")
async def get_comprehensive_stats():
    """Get detailed system statistics"""
    try:
        # Activity statistics
        activity_stats = {}
        priority_distribution = {}
        duration_stats = {"total_minutes": 0, "average_duration": 0}
        
        for activity in scheduler.activities:
            activity_type = activity.activity_type.value
            activity_stats[activity_type] = activity_stats.get(activity_type, 0) + 1
            
            priority_distribution[activity.priority] = priority_distribution.get(activity.priority, 0) + 1
            duration_stats["total_minutes"] += activity.duration_minutes
        
        if scheduler.activities:
            duration_stats["average_duration"] = duration_stats["total_minutes"] / len(scheduler.activities)
        
        # Resource statistics
        resource_stats = {}
        availability_stats = {"high": 0, "medium": 0, "low": 0}
        
        for resource in scheduler.resources:
            resource_type = resource.resource_type
            resource_stats[resource_type] = resource_stats.get(resource_type, 0) + 1
            
            availability_pct = len(resource.available_dates) / 90 * 100  # 90 days
            if availability_pct > 80:
                availability_stats["high"] += 1
            elif availability_pct > 50:
                availability_stats["medium"] += 1
            else:
                availability_stats["low"] += 1
        
        # Scheduling statistics
        scheduling_stats = {
            "scheduled_activities": len(scheduler.scheduled_activities),
            "conflicts": len(scheduler.scheduling_conflicts),
            "unscheduled": len(scheduler.unscheduled_activities),
            "success_rate": 0
        }
        
        if scheduler.activities:
            scheduling_stats["success_rate"] = len(scheduler.scheduled_activities) / len(scheduler.activities) * 100
        
        # Client constraint statistics
        client_stats = {}
        if scheduler.client_schedule:
            client_stats = {
                "travel_days": len(scheduler.client_schedule.travel_dates),
                "busy_periods": len(scheduler.client_schedule.busy_periods),
                "preferred_time_slots": len(scheduler.client_schedule.preferred_times),
                "blackout_days": len(getattr(scheduler.client_schedule, 'blackout_dates', []))
            }
        
        return {
            "system_overview": {
                "total_activities": len(scheduler.activities),
                "total_resources": len(scheduler.resources),
                "data_initialized": data_initialized,
                "last_updated": datetime.now().isoformat()
            },
            "activities": {
                "by_type": activity_stats,
                "by_priority": priority_distribution,
                "duration": duration_stats
            },
            "resources": {
                "by_type": resource_stats,
                "availability_distribution": availability_stats
            },
            "scheduling": scheduling_stats,
            "client_constraints": client_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating statistics: {str(e)}")

@app.get("/health")
async def health_check():
    """Enhanced health check with system status"""
    try:
        system_status = "healthy"
        issues = []
        
        if not data_initialized:
            system_status = "warning"
            issues.append("Data not initialized")
        
        if not scheduler.activities:
            system_status = "error"
            issues.append("No activities loaded")
        
        if not scheduler.resources:
            system_status = "error"
            issues.append("No resources loaded")
        
        return {
            "status": system_status,
            "timestamp": datetime.now().isoformat(),
            "data_status": {
                "initialized": data_initialized,
                "activities_loaded": len(scheduler.activities),
                "resources_loaded": len(scheduler.resources),
                "client_schedule_loaded": scheduler.client_schedule is not None
            },
            "scheduling_status": {
                "last_scheduled_count": len(scheduler.scheduled_activities),
                "conflicts": len(scheduler.scheduling_conflicts),
                "unscheduled": len(scheduler.unscheduled_activities)
            },
            "issues": issues
        }
        
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/reset-data")
async def reset_data():
    """Reset and regenerate all sample data"""
    try:
        global data_initialized
        data_initialized = False
        
        # Clear current data
        scheduler.activities = []
        scheduler.resources = []
        scheduler.client_schedule = None
        scheduler.scheduled_activities = []
        
        # Regenerate
        initialize_data()
        
        return {
            "message": "Data successfully reset and regenerated",
            "new_counts": {
                "activities": len(scheduler.activities),
                "resources": len(scheduler.resources)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting data: {str(e)}")
    
@app.get("/data/{filename}")
async def get_data_file(filename: str):
    """Serve data files"""
    try:
        filepath = f"data/{filename}"
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")