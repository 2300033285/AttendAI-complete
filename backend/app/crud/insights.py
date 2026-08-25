from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.employee import Employee
from app.models.attendance import Attendance

from app.crud.shift_analytics import get_shift_analytics
from app.crud.anomaly import get_anomalies
from app.crud.ai_prediction import get_ai_prediction


def get_insights(db: Session):

    # -----------------------------------------
    # 1. EMPLOYEE ANALYTICS
    # -----------------------------------------

    total_employees = db.query(Employee).count()

    active_employees = (
        db.query(Employee)
        .filter(Employee.status == True)
        .count()
    )

    # -----------------------------------------
    # 2. ATTENDANCE ANALYTICS
    # -----------------------------------------

    total_attendance = db.query(Attendance).count()

    present_attendance = (
        db.query(Attendance)
        .filter(func.lower(Attendance.status) == "present")
        .count()
    )

    attendance_percentage = 0

    if total_attendance > 0:
        attendance_percentage = round(
            (present_attendance / total_attendance) * 100,
            2
        )

    # -----------------------------------------
    # 3. DEPARTMENT SUMMARY
    # -----------------------------------------

    department_data = (
        db.query(
            Employee.department,
            func.count(Employee.id)
        )
        .group_by(Employee.department)
        .all()
    )

    department_summary = {
        dept: count
        for dept, count in department_data
    }

    # -----------------------------------------
    # 4. DESIGNATION SUMMARY
    # -----------------------------------------

    designation_data = (
        db.query(
            Employee.designation,
            func.count(Employee.id)
        )
        .group_by(Employee.designation)
        .all()
    )

    designation_summary = {
        designation: count
        for designation, count in designation_data
    }

    # -----------------------------------------
    # 5. SHIFT ANALYTICS
    # -----------------------------------------

    shift_analytics = get_shift_analytics(db)

    # -----------------------------------------
    # 6. ANOMALY DETECTION
    # -----------------------------------------

    anomaly_data = get_anomalies(db)

    # -----------------------------------------
    # 7. AI PREDICTION
    # -----------------------------------------

    ai_prediction = get_ai_prediction(db, 2)
    
    print("AI PREDICTION:", ai_prediction)

    # -----------------------------------------
    # 8. FINAL INSIGHTS
    # -----------------------------------------

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "attendance_percentage": attendance_percentage,
        "department_summary": department_summary,
        "designation_summary": designation_summary,
        "shift_analytics": shift_analytics,
        "anomalies": anomaly_data,
        "ai_prediction": ai_prediction
    }