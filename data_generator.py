import json
import os
from datetime import datetime, date, timedelta
from typing import List
import random
from models import Activity, ActivityType, ResourceAvailability, ClientSchedule

class DataGenerator:
    def __init__(self):
        self.fitness_data = [
            {"name": "Morning Run", "details": "30-45 min cardio, HR 120-140 bpm", "location": "Park"},
            {"name": "Weight Training", "details": "3 sets x 12 reps, progressive overload", "location": "Gym"},
            {"name": "Yoga Flow", "details": "60 min vinyasa, focus on flexibility", "location": "Studio"},
            {"name": "Swimming", "details": "45 min laps, technique focus", "location": "Pool"},
            {"name": "HIIT Workout", "details": "20 min high intensity intervals", "location": "Gym"},
            {"name": "Pilates", "details": "Core strengthening, 45 minutes", "location": "Studio"},
            {"name": "Cycling", "details": "60 min endurance ride", "location": "Outdoors"},
            {"name": "Stretching Session", "details": "30 min full body flexibility", "location": "Home"},
            {"name": "Balance Training", "details": "Stability and coordination work", "location": "Gym"},
            {"name": "Eye Exercises", "details": "Vision therapy, 15 minutes", "location": "Home"},
            {"name": "Walking Meditation", "details": "Mindful walking, 30 minutes", "location": "Park"},
            {"name": "Resistance Band Training", "details": "Full body resistance workout", "location": "Home"},
            {"name": "CrossFit WOD", "details": "Workout of the day, varied movements", "location": "CrossFit Box"},
            {"name": "Tai Chi", "details": "Slow controlled movements, balance", "location": "Park"},
            {"name": "Dance Fitness", "details": "Cardio through dance, 45 minutes", "location": "Studio"},
            {"name": "Rock Climbing", "details": "Strength and problem solving", "location": "Climbing Gym"},
            {"name": "Martial Arts", "details": "Self-defense and fitness", "location": "Dojo"},
            {"name": "Aqua Aerobics", "details": "Low impact water exercises", "location": "Pool"},
            {"name": "Functional Movement", "details": "Daily life movement patterns", "location": "Gym"},
            {"name": "Foam Rolling", "details": "Myofascial release, recovery", "location": "Home"},
            {"name": "Kettlebell Training", "details": "Compound movements, strength", "location": "Gym"},
            {"name": "Barre Class", "details": "Ballet-inspired fitness", "location": "Studio"},
            {"name": "Spin Class", "details": "Indoor cycling with music", "location": "Gym"},
            {"name": "TRX Suspension", "details": "Bodyweight resistance training", "location": "Gym"},
            {"name": "Breathwork Session", "details": "Controlled breathing exercises", "location": "Home"}
        ]
        
        self.food_data = [
            {"name": "Mediterranean Breakfast", "details": "High omega-3, antioxidants, 400-500 cal"},
            {"name": "Protein Power Bowl", "details": "35g protein minimum, vegetables"},
            {"name": "Anti-inflammatory Smoothie", "details": "Berries, spinach, turmeric, ginger"},
            {"name": "Quinoa Buddha Bowl", "details": "Complete proteins, fiber-rich"},
            {"name": "Wild Salmon Dinner", "details": "Omega-3 rich, with vegetables"},
            {"name": "Green Detox Juice", "details": "Kale, cucumber, celery, lemon"},
            {"name": "Chia Seed Pudding", "details": "High fiber, omega-3, probiotics"},
            {"name": "Bone Broth", "details": "Collagen, minerals, gut health"},
            {"name": "Fermented Foods", "details": "Kimchi, sauerkraut, gut microbiome"},
            {"name": "Nuts and Seeds Mix", "details": "Healthy fats, vitamin E, minerals"},
            {"name": "Herbal Tea Blend", "details": "Adaptogenic herbs, caffeine-free"},
            {"name": "Avocado Toast", "details": "Healthy fats, fiber, whole grains"},
            {"name": "Greek Yogurt Parfait", "details": "Probiotics, protein, antioxidants"},
            {"name": "Sweet Potato Bowl", "details": "Beta-carotene, fiber, complex carbs"},
            {"name": "Cruciferous Vegetables", "details": "Broccoli, cauliflower, detox support"},
            {"name": "Berry Antioxidant Bowl", "details": "Blueberries, strawberries, vitamin C"},
            {"name": "Lean Protein Meal", "details": "Chicken, fish, or plant protein"},
            {"name": "Hydration Boost", "details": "Electrolyte water, coconut water"},
            {"name": "Prebiotic Foods", "details": "Garlic, onions, gut health support"},
            {"name": "Magnesium-Rich Meal", "details": "Dark leafy greens, nuts, seeds"},
            {"name": "B-Vitamin Complex Foods", "details": "Nutritional yeast, eggs, legumes"},
            {"name": "Calcium-Rich Meal", "details": "Sesame seeds, almonds, leafy greens"},
            {"name": "Iron Absorption Meal", "details": "Vitamin C with iron-rich foods"},
            {"name": "Zinc-Rich Foods", "details": "Pumpkin seeds, oysters, beans"},
            {"name": "Selenium Sources", "details": "Brazil nuts, seafood, whole grains"},
            {"name": "Potassium-Rich Foods", "details": "Bananas, potatoes, spinach"},
            {"name": "Fiber Power Meal", "details": "Beans, lentils, vegetables"},
            {"name": "Healthy Fats Meal", "details": "Olive oil, nuts, fatty fish"},
            {"name": "Low Glycemic Meal", "details": "Stable blood sugar, complex carbs"},
            {"name": "Alkalizing Foods", "details": "pH balance, vegetables, fruits"}
        ]

    def generate_activities(self, count: int = 120) -> List[Activity]:
        activities = []
        activity_id = 1
        
        # Fitness activities (25)
        for i, fitness in enumerate(self.fitness_data):
            if len(activities) >= count * 0.25:
                break
            activity = Activity(
                id=activity_id,
                activity_type=ActivityType.FITNESS,
                name=fitness["name"],
                priority=random.randint(1, 8),
                frequency=random.choice([
                    "daily", "3 times a week", "5 times a week", "twice a week",
                    "4 times a week", "6 times a week", "every other day"
                ]),
                details=fitness["details"],
                facilitator=random.choice([
                    "Personal Trainer", "Yoga Instructor", "Self", "Fitness Coach",
                    "Physical Therapist", "Group Instructor"
                ]),
                location=fitness["location"],
                remote_capable=random.choice([True, False]),
                duration_minutes=random.choice([30, 45, 60, 90]),
                prep_required=random.choice([
                    "Prepare workout clothes and water",
                    "Warm-up for 5-10 minutes",
                    "Check equipment availability",
                    "Light snack 1 hour before"
                ]),
                backup_activities=["Bodyweight exercises", "Stretching routine", "Walking"],
                skip_adjustments="Add 15 minutes to next session",
                metrics=["Heart Rate", "Duration", "Calories", "Performance Score"]
            )
            activities.append(activity)
            activity_id += 1
        
        # Food activities (30)
        for i, food in enumerate(self.food_data):
            if len(activities) >= 25 + count * 0.30:
                break
            activity = Activity(
                id=activity_id,
                activity_type=ActivityType.FOOD,
                name=food["name"],
                priority=random.randint(1, 6),
                frequency=random.choice([
                    "daily", "twice daily", "3 times daily", "weekly",
                    "5 times a week", "every meal", "twice a week"
                ]),
                details=food["details"],
                facilitator=random.choice([
                    "Self", "Nutritionist", "Meal Prep Service", "Chef", "Family"
                ]),
                location=random.choice(["Home", "Kitchen", "Restaurant", "Office"]),
                remote_capable=False,
                duration_minutes=random.choice([15, 30, 45, 60]),
                prep_required=random.choice([
                    "Shop for fresh ingredients",
                    "Meal prep on Sunday",
                    "Defrost proteins overnight",
                    "Wash and chop vegetables"
                ]),
                backup_activities=["Healthy meal replacement", "Smoothie alternative"],
                skip_adjustments="Include missed nutrients in next meal",
                metrics=["Calories", "Macros", "Satisfaction", "Energy Level"]
            )
            activities.append(activity)
            activity_id += 1
        
        # Generate remaining activities (medications, therapy, consultations)
        self._generate_remaining_activities(activities, activity_id, count)
        
        return activities[:count]

    def _generate_remaining_activities(self, activities, start_id, total_count):
        current_id = start_id
        
        # Medications (25)
        medications = [
            "Vitamin D3", "Omega-3 Fish Oil", "Multivitamin", "Magnesium",
            "Probiotics", "Vitamin B12", "Calcium + D3", "Coenzyme Q10",
            "Turmeric Supplement", "Zinc", "Iron", "Vitamin C", "Folate",
            "Biotin", "Chromium", "Selenium", "Iodine", "Potassium",
            "Ashwagandha", "Rhodiola", "Melatonin", "Digestive Enzymes",
            "Green Tea Extract", "Resveratrol", "Curcumin"
        ]
        
        for med in medications:
            if len(activities) >= total_count * 0.75:
                break
            activities.append(Activity(
                id=current_id,
                activity_type=ActivityType.MEDICATION,
                name=f"{med} Supplement",
                priority=random.randint(2, 8),
                frequency=random.choice(["daily", "twice daily", "with meals", "weekly"]),
                details=f"Take {med} as directed, monitor for effects",
                facilitator="Self",
                location="Home",
                remote_capable=False,
                duration_minutes=5,
                prep_required="Ensure medication supply available",
                backup_activities=["Consult pharmacist for alternatives"],
                skip_adjustments="Take next dose at regular time",
                metrics=["Adherence", "Side Effects", "Biomarker Changes"]
            ))
            current_id += 1
        
        # Therapy activities
        therapies = [
            "Sauna Session", "Ice Bath", "Massage Therapy", "Acupuncture",
            "Red Light Therapy", "Compression Therapy", "Cryotherapy",
            "Infrared Sauna", "Lymphatic Drainage", "Cupping Therapy",
            "Reflexology", "Chiropractic", "Osteopathy", "Reiki",
            "Sound Therapy", "Aromatherapy", "Meditation", "Float Tank",
            "Hyperbaric Oxygen", "PEMF Therapy"
        ]
        
        for therapy in therapies:
            if len(activities) >= total_count * 0.9:
                break
            activities.append(Activity(
                id=current_id,
                activity_type=ActivityType.THERAPY,
                name=therapy,
                priority=random.randint(3, 9),
                frequency=random.choice(["weekly", "twice a week", "monthly", "bi-weekly"]),
                details=f"{therapy} session for recovery and wellness",
                facilitator=random.choice([
                    "Licensed Therapist", "Certified Practitioner", "Wellness Center"
                ]),
                location=random.choice(["Spa", "Clinic", "Wellness Center", "Home"]),
                remote_capable=False,
                duration_minutes=random.choice([30, 45, 60, 90]),
                prep_required="Arrive 10 minutes early, hydrate well",
                backup_activities=["Self-massage", "Hot bath", "Relaxation techniques"],
                skip_adjustments="Reschedule within same week if possible",
                metrics=["Pain Level", "Stress Level", "Mobility", "Sleep Quality"]
            ))
            current_id += 1
        
        # Consultations
        consultations = [
            "Nutritionist Consultation", "Personal Training Session",
            "Physiotherapy", "Health Coaching", "Mental Health Counseling",
            "Cardiologist Checkup", "Blood Work Review", "Fitness Assessment",
            "Body Composition Analysis", "Stress Management Session",
            "Sleep Specialist", "Endocrinologist Visit", "Dermatology Checkup"
        ]
        
        for consultation in consultations:
            if len(activities) >= total_count:
                break
            activities.append(Activity(
                id=current_id,
                activity_type=ActivityType.CONSULTATION,
                name=consultation,
                priority=random.randint(1, 7),
                frequency=random.choice(["monthly", "bi-weekly", "quarterly", "weekly"]),
                details=f"Professional {consultation.lower()} session",
                facilitator=f"Licensed {consultation.split()[0]} Professional",
                location=random.choice(["Clinic", "Office", "Online", "Hospital"]),
                remote_capable=random.choice([True, False]),
                duration_minutes=random.choice([30, 45, 60]),
                prep_required="Prepare questions and health history",
                backup_activities=["Telehealth consultation", "Reschedule priority"],
                skip_adjustments="Priority reschedule within 48 hours",
                metrics=["Goals Progress", "Action Items", "Satisfaction"]
            ))
            current_id += 1

    def generate_resource_availability(self, start_date: date, months: int = 3) -> List[ResourceAvailability]:
        resources = []
        end_date = start_date + timedelta(days=months * 30)
        
        # Equipment
        equipment = [
            {"name": "Gym Access", "capacity": 50},
            {"name": "Pool Access", "capacity": 20},
            {"name": "Sauna", "capacity": 8},
            {"name": "Massage Tables", "capacity": 4},
            {"name": "Yoga Studio", "capacity": 15},
            {"name": "Personal Training Room", "capacity": 2},
            {"name": "Cycling Equipment", "capacity": 12},
            {"name": "Weight Training Area", "capacity": 20}
        ]
        
        for eq in equipment:
            available_dates = self._generate_availability_dates(start_date, end_date, 0.85)
            resources.append(ResourceAvailability(
                resource_type="equipment",
                resource_id=f"eq_{eq['name'].lower().replace(' ', '_')}",
                name=eq['name'],
                available_dates=available_dates,
                available_times=["06:00-22:00"],
                capacity=eq['capacity']
            ))
        
        # Specialists
        specialists = [
            "Dr. Smith - Cardiologist",
            "Jane Doe - Personal Trainer", 
            "Mike Johnson - Massage Therapist",
            "Sarah Wilson - Nutritionist",
            "David Brown - Physiotherapist",
            "Lisa Garcia - Mental Health Counselor",
            "Tom Anderson - Fitness Coach",
            "Maria Rodriguez - Yoga Instructor"
        ]
        
        for spec in specialists:
            available_dates = self._generate_availability_dates(start_date, end_date, 0.7, weekdays_only=True)
            resources.append(ResourceAvailability(
                resource_type="specialist",
                resource_id=f"spec_{spec.split()[0].lower()}_{spec.split()[1].lower()}",
                name=spec,
                available_dates=available_dates,
                available_times=["09:00-12:00", "14:00-17:00"],
                capacity=1
            ))
        
        # Allied Health
        allied_health = [
            "Physical Therapist - Anna",
            "Occupational Therapist - Bob",
            "Registered Dietitian - Carol",
            "Speech Therapist - Dan",
            "Exercise Physiologist - Eve"
        ]
        
        for ah in allied_health:
            available_dates = self._generate_availability_dates(start_date, end_date, 0.75, include_saturdays=True)
            resources.append(ResourceAvailability(
                resource_type="allied_health",
                resource_id=f"ah_{ah.split()[-1].lower()}",
                name=ah,
                available_dates=available_dates,
                available_times=["08:00-16:00"],
                capacity=1
            ))
        
        return resources

    def _generate_availability_dates(self, start_date: date, end_date: date, availability_rate: float, 
                                   weekdays_only: bool = False, include_saturdays: bool = False) -> List[date]:
        available_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            include_date = True
            
            if weekdays_only and current_date.weekday() >= 5:  # Weekend
                include_date = False
            elif not weekdays_only and not include_saturdays and current_date.weekday() == 6:  # Sunday only
                include_date = False
            
            if include_date and random.random() < availability_rate:
                available_dates.append(current_date)
            
            current_date += timedelta(days=1)
        
        return available_dates

    def generate_client_schedule(self, start_date: date, months: int = 3) -> ClientSchedule:
        end_date = start_date + timedelta(days=months * 30)
        busy_periods = []
        travel_dates = []
        blackout_dates = []
        
        # Work schedule (Monday-Friday, 9-5)
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Weekdays
                busy_periods.append({
                    "date": current_date.isoformat(),
                    "start_time": "09:00",
                    "end_time": "17:00",
                    "description": "Work"
                })
            current_date += timedelta(days=1)
        
        # Travel periods
        for _ in range(random.randint(2, 4)):
            travel_start = start_date + timedelta(days=random.randint(0, months * 30 - 10))
            trip_length = random.randint(3, 8)
            for i in range(trip_length):
                travel_date = travel_start + timedelta(days=i)
                if travel_date <= end_date:
                    travel_dates.append(travel_date)
        
        # Some random blackout dates (sick days, personal commitments)
        for _ in range(random.randint(3, 8)):
            blackout_date = start_date + timedelta(days=random.randint(0, months * 30))
            if blackout_date <= end_date:
                blackout_dates.append(blackout_date)
        
        return ClientSchedule(
            busy_periods=busy_periods,
            travel_dates=travel_dates,
            preferred_times=["06:00-08:00", "12:00-13:00", "18:00-20:00"],
            blackout_dates=blackout_dates
        )

    def save_data_to_files(self):
        os.makedirs('data', exist_ok=True)
        start_date = date.today()
        
        try:
            # Generate activities
            activities = self.generate_activities(120)
            activities_data = []
            for activity in activities:
                activity_dict = activity.dict()
                activities_data.append(activity_dict)
            
            with open('data/activities.json', 'w') as f:
                json.dump(activities_data, f, indent=2, default=str)
            
            # Generate resources
            resources = self.generate_resource_availability(start_date, 3)
            resources_data = []
            for resource in resources:
                resource_dict = resource.dict()
                # Convert dates to strings for JSON serialization
                resource_dict['available_dates'] = [d.isoformat() for d in resource_dict['available_dates']]
                resources_data.append(resource_dict)
            
            with open('data/resources.json', 'w') as f:
                json.dump(resources_data, f, indent=2, default=str)
            
            # Generate client schedule
            client_schedule = self.generate_client_schedule(start_date, 3)
            client_dict = client_schedule.dict()
            client_dict['travel_dates'] = [d.isoformat() for d in client_dict['travel_dates']]
            client_dict['blackout_dates'] = [d.isoformat() for d in client_dict['blackout_dates']]
            
            with open('data/client_schedule.json', 'w') as f:
                json.dump(client_dict, f, indent=2, default=str)
            
            print(f"✅ Generated {len(activities)} activities")
            print(f"✅ Generated {len(resources)} resource availability records")
            print(f"✅ Generated client schedule with {len(client_schedule.travel_dates)} travel dates")
            
            return activities, resources, client_schedule
            
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            raise

if __name__ == "__main__":
    generator = DataGenerator()
    generator.save_data_to_files()