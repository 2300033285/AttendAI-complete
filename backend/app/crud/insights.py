from sqlalchemy.orm import Session

from app.crud.employee_analytics import get_employee_analytics
from app.crud.analytics import get_analytics
from app.crud.shift_analytics import get_shift_analytics
from app.crud.attendance_anomaly import get_anomalies
from app.crud.ai_prediction import get_ai_prediction

from app.services.leave_anomaly_service import detect_leave_anomalies
from app.services.referral_anomaly_service import detect_referral_anomalies

from app.models.employee import Employee
from app.models.user import User


def get_insights(db: Session):

    # =====================================================
    # 1. EMPLOYEE ANALYTICS
    # =====================================================

    employee_data = get_employee_analytics(db)

    total_employees = employee_data["total_employees"]
    active_employees = employee_data["active_employees"]

    department_summary = employee_data[
        "department_count"
    ]

    designation_summary = employee_data[
        "designation_count"
    ]

    # =====================================================
    # 2. ATTENDANCE ANALYTICS
    # =====================================================

    attendance_data = get_analytics(db)

    attendance_percentage = attendance_data[
        "attendance_percentage"
    ]

    # =====================================================
    # 3. SHIFT ANALYTICS
    # =====================================================

    shift_analytics = get_shift_analytics(db)

    # =====================================================
    # 4. ATTENDANCE ANOMALIES
    # =====================================================

    attendance_anomalies = get_anomalies(db)

    # =====================================================
    # 5. LEAVE ANOMALIES
    # =====================================================

    leave_anomalies = []

    employees = (
        db.query(Employee)
        .all()
    )

    for employee in employees:

        leave_result = detect_leave_anomalies(
            db=db,
            employee_id=employee.id
        )

        if leave_result["anomaly_detected"]:

            leave_anomalies.append(
                leave_result
            )

    # =====================================================
    # 6. REFERRAL ANOMALIES
    # =====================================================

    referral_anomalies = []

    for employee in employees:

        referral_result = detect_referral_anomalies(
            db=db,
            employee_id=employee.id
        )

        if referral_result["anomaly_detected"]:

            referral_anomalies.append(
                referral_result
            )

    # =====================================================
    # 7. COMBINED ANOMALIES
    # =====================================================

    anomaly_data = {
        "attendance": attendance_anomalies,
        "leave": {
            "total_anomalies": len(
                leave_anomalies
            ),
            "anomalies": leave_anomalies,
        },
        "referral": {
            "total_anomalies": len(
                referral_anomalies
            ),
            "anomalies": referral_anomalies,
        },
    }

    # =====================================================
    # 8. AI PREDICTION
    # =====================================================

    # Use the first available employee user
    employee_user = (
        db.query(User)
        .filter(
            User.role.ilike("Employee")
        )
        .first()
    )

    if employee_user:

        ai_prediction = get_ai_prediction(
            db,
            employee_user.id
        )

    else:

        ai_prediction = {
            "prediction": "No Data",
            "confidence": 0
        }

    # =====================================================
    # 9. FINAL DASHBOARD INSIGHTS
    # =====================================================

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "attendance_percentage": attendance_percentage,
        "department_summary": department_summary,
        "designation_summary": designation_summary,
        "shift_analytics": shift_analytics,
        "anomalies": anomaly_data,
        "ai_prediction": ai_prediction,
    }