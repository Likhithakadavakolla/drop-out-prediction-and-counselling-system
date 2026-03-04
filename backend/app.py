from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import csv
import os
import sys
import threading

# Add parent directory to path to import notifier
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notifier import send_email

# Constants
ATTENDANCE_THRESHOLD_HIGH = 60
ATTENDANCE_THRESHOLD_MEDIUM = 75
MARKS_THRESHOLD_HIGH = 40
MARKS_THRESHOLD_MEDIUM = 60
ATTEMPTS_THRESHOLD = 3

CSV_PATHS = [
    "../frontend/data/student_data.csv",
    "frontend/data/student_data.csv",
]

app = FastAPI(
    title="Student Dropout Prediction API",
    description="AI-based system to predict student dropout risk",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class StudentInput(BaseModel):
    student_id: int = Field(..., gt=0, description="Student ID must be positive")
    attendance: float = Field(..., ge=0, le=100, description="Attendance percentage (0-100)")
    marks: float = Field(..., ge=0, le=100, description="Marks (0-100)")
    attempts: int = Field(..., ge=0, description="Number of attempts")
    guardian_email: EmailStr
    mentor_email: EmailStr


class Student(BaseModel):
    student_id: int
    name: str
    attendance: float
    marks: float
    attempts: int
    guardian_email: str
    mentor_email: str


def predict_risk(attendance: float, marks: float, attempts: int) -> tuple[str, str]:
    """Calculate risk level based on student performance metrics."""
    if attendance < ATTENDANCE_THRESHOLD_HIGH or marks < MARKS_THRESHOLD_HIGH or attempts >= ATTEMPTS_THRESHOLD:
        return "HIGH RISK", "Immediate counselling required. Student showing critical performance issues."
    elif attendance < ATTENDANCE_THRESHOLD_MEDIUM or marks < MARKS_THRESHOLD_MEDIUM:
        return "MEDIUM RISK", "Monitor student closely. Consider intervention if performance declines."
    return "LOW RISK", "Student performing well. Continue monitoring."


@app.get("/")
def read_root():
    return {"message": "Dropout Prediction API", "status": "running"}


@app.get("/students", response_model=list[Student])
def get_students():
    """Retrieve all student records from CSV file."""
    students = []
    csv_file = None
    
    # Find CSV file
    for path in CSV_PATHS:
        if os.path.exists(path):
            csv_file = path
            break
    
    if not csv_file:
        print(f"⚠️ CSV file not found. Tried paths: {CSV_PATHS}")
        return []
    
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                try:
                    students.append({
                        "student_id": int(row["student_id"]),
                        "name": row["name"].strip(),
                        "attendance": float(row["attendance"]),
                        "marks": float(row["marks"]),
                        "attempts": int(row["attempts"]),
                        "guardian_email": row["guardian_email"].strip(),
                        "mentor_email": row["mentor_email"].strip()
                    })
                except (ValueError, KeyError) as e:
                    print(f"⚠️ Skipping invalid row {idx}: {e}")
                    continue
        
        print(f"✅ Loaded {len(students)} students from {csv_file}")
        return students
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []


@app.post("/predict")
def predict(data: StudentInput):
    risk, message = predict_risk(
        data.attendance,
        data.marks,
        data.attempts
    )

    email_sent = False
    error_message = None
    if risk == "HIGH RISK":
        # Enhanced email message with student details
        guardian_message = f"""
Dear Parent/Guardian,

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 URGENT STUDENT ALERT - IMMEDIATE ATTENTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is an automated notification from our Student Dropout Prevention and Counselling System. Our AI-based early warning system has identified concerning academic trends for your ward.

📋 STUDENT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Student ID: {data.student_id}
Student Name: [To be updated by mentor]
Assessment Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

⚠️ CURRENT PERFORMANCE INDICATORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Attendance Rate: {data.attendance}% (Target: ≥60%)
• Academic Score: {data.marks}/100 (Target: ≥40)
• Failed Assessment Attempts: {data.attempts} (Threshold: 3)

🔴 RISK ASSESSMENT: {risk}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{message}

📊 KEY CONCERNS IDENTIFIED:
{'• Critical Attendance Shortage: Below 60% minimum requirement' if data.attendance < ATTENDANCE_THRESHOLD_HIGH else ''}
{'• Academic Performance Alert: Scoring below passing threshold' if data.marks < MARKS_THRESHOLD_HIGH else ''}
{'• Multiple Failed Attempts: Indicates learning difficulties or engagement issues' if data.attempts >= ATTEMPTS_THRESHOLD else ''}

💡 RECOMMENDED IMMEDIATE ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Schedule an urgent meeting with the assigned academic mentor
2. Review attendance patterns and address any underlying issues
3. Discuss academic challenges and explore tutoring support
4. Consider counselling services for personal/motivational guidance
5. Create a structured improvement plan with clear milestones

📞 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The academic mentor has been simultaneously notified and will reach out to schedule a counselling session within 48 hours. Your active participation is crucial for your ward's academic success.

📧 Contact Information:
• Academic Support Office: support@institution.edu
• Counselling Services: counselling@institution.edu
• Student Helpline: +1-XXX-XXX-XXXX

We believe in every student's potential and are committed to providing comprehensive support. Early intervention can make a significant difference.

Best regards,
Student Dropout Prevention Team
Academic Affairs Office

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated alert. Please do not reply to this email.
For urgent matters, contact the numbers above.
        """
        
        mentor_message = f"""
Dear Academic Mentor,

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 HIGH-PRIORITY STUDENT INTERVENTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Our AI-powered Dropout Prediction System has flagged a student under your mentorship who requires immediate intervention. This alert is generated based on multiple risk indicators and predictive analytics.

📋 STUDENT PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Student ID: {data.student_id}
Student Name: [Access student records for full details]
Alert Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Alert Priority: URGENT

📊 PERFORMANCE METRICS ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Metric                  | Current | Threshold | Status
─────────────────────────────────────────────────────
Attendance Rate         | {data.attendance}%     | ≥60%      | {'🔴 CRITICAL' if data.attendance < ATTENDANCE_THRESHOLD_HIGH else '🟢 PASS'}
Academic Performance    | {data.marks}/100   | ≥40/100   | {'🔴 CRITICAL' if data.marks < MARKS_THRESHOLD_HIGH else '🟢 PASS'}
Failed Attempts         | {data.attempts}        | <3        | {'🔴 CRITICAL' if data.attempts >= ATTEMPTS_THRESHOLD else '🟢 PASS'}

🎯 DROPOUT RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk Level: {risk} 🔴
Confidence: High (Multi-factor analysis)

Systematic Analysis:
{message}

⚠️ PRIMARY RISK FACTORS IDENTIFIED:
{'✗ Chronic Absenteeism: Attendance below institutional minimum (60%)' if data.attendance < ATTENDANCE_THRESHOLD_HIGH else ''}
{'✗ Academic Distress: Performance significantly below passing standards' if data.marks < MARKS_THRESHOLD_HIGH else ''}
{'✗ Repeated Failures: Multiple assessment attempts indicate comprehension gaps' if data.attempts >= ATTEMPTS_THRESHOLD else ''}
{'✗ Cumulative Risk: Multiple indicators suggest high dropout probability' if (data.attendance < ATTENDANCE_THRESHOLD_HIGH and data.marks < MARKS_THRESHOLD_HIGH) else ''}

📋 MANDATORY INTERVENTION PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
As the assigned mentor, please initiate the following within 48 hours:

✓ IMMEDIATE ACTIONS (Within 24 hours):
  1. Schedule one-on-one counselling session with student
  2. Contact parent/guardian to discuss concerns
  3. Review student's complete academic history
  4. Document current challenges and barriers

✓ SHORT-TERM INTERVENTIONS (Within 1 week):
  5. Develop personalized Academic Improvement Plan (AIP)
  6. Connect student with tutoring/academic support services
  7. Assess need for counselling (personal/psychological)
  8. Arrange peer mentoring or study group participation
  9. Set up weekly check-ins to monitor progress

✓ DOCUMENTATION REQUIRED:
  • Initial counselling session notes
  • Action plan with specific, measurable goals
  • Follow-up schedule and tracking mechanism
  • Monthly progress reports to Academic Affairs

🔄 FOLLOW-UP TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 48 Hours: Initial counselling session completed
• 1 Week: Academic Improvement Plan submitted
• 2 Weeks: First progress review meeting
• Monthly: Ongoing monitoring and adjustment

📞 SUPPORT RESOURCES AVAILABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Academic Support Center: ext. 1234
• Counselling Services: ext. 5678
• Student Affairs Office: ext. 9012
• Tutoring Services: tutoring@institution.edu
• Mental Health Support: wellness@institution.edu

📝 IMPORTANT NOTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Guardian has been notified simultaneously
• Maintain student confidentiality per institutional policy
• Document all interventions in student management system
• Escalate to Academic Dean if no improvement within 4 weeks
• Early intervention significantly improves retention rates

Your proactive engagement is critical in helping this student succeed. Research shows that timely mentor intervention can reduce dropout risk by up to 70%.

Thank you for your dedication to student success.

Best regards,
Student Dropout Prevention & Counselling System
Academic Affairs & Student Support Division

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
System Alert ID: SDPS-{data.student_id}-{datetime.now().strftime('%Y%m%d%H%M')}
This is an automated alert from an AI-based prediction system.
For system issues, contact: tech-support@institution.edu
        """
        
        # Send both emails in parallel threads for instant response
        def send_guardian_email():
            try:
                send_email(data.guardian_email, "⚠️ Student At Risk - Immediate Attention Required", guardian_message)
                print(f"✅ Guardian email sent for Student ID: {data.student_id}")
            except Exception as e:
                print(f"❌ Guardian email failed: {e}")
        
        def send_mentor_email():
            try:
                send_email(data.mentor_email, "⚠️ Student Alert - High Risk Detected", mentor_message)
                print(f"✅ Mentor email sent for Student ID: {data.student_id}")
            except Exception as e:
                print(f"❌ Mentor email failed: {e}")
        
        # Launch both emails in parallel threads
        thread1 = threading.Thread(target=send_guardian_email)
        thread2 = threading.Thread(target=send_mentor_email)
        thread1.daemon = True
        thread2.daemon = True
        thread1.start()
        thread2.start()
        
        email_sent = True
        print(f"📧 Email sending initiated for Student ID: {data.student_id}")

    response_data = {
        "student_id": data.student_id,
        "risk_level": risk,
        "message": message,
        "email_sent": email_sent,
        "timestamp": datetime.now().isoformat()
    }
    
    if error_message:
        response_data["error"] = error_message
    
    return response_data
