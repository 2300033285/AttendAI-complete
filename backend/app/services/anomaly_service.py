from sqlalchemy.orm import Session

from app.crud.attendance_anomaly import get_anomalies
from app.services.leave_anomaly_service import detect_leave_anomalies
from app.services.referral_anomaly_service import detect_referral_anomalies
from app.models.employee import Employee
from app.models.user import User


def anomaly_service(db: Session):
    return get_anomalies(db)


def employee_anomaly_service(
    db: Session,
    employee_id: int
):
    # Verify employee exists
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None

    # Find user linked to this employee
    user = (
        db.query(User)
        .filter(User.employee_id == str(employee_id))
        .first()
    )

    # Attendance anomalies
    attendance_result = get_anomalies(db)

    attendance_anomalies = []

    if user:
        attendance_anomalies = [
            anomaly
            for anomaly in attendance_result["anomalies"]
            if anomaly["user_id"] == user.id
        ]

    # Leave anomalies
    leave_result = detect_leave_anomalies(
        db=db,
        employee_id=employee_id
    )

    # Referral anomalies
    referral_result = detect_referral_anomalies(
        db=db,
        employee_id=employee_id
    )

    total_anomalies = (
        len(attendance_anomalies)
        + (1 if leave_result["anomaly_detected"] else 0)
        + (1 if referral_result["anomaly_detected"] else 0)
    )

    return {
        "employee_id": employee_id,
        "total_anomalies": total_anomalies,
        "attendance_anomalies": attendance_anomalies,
        "leave_anomalies": leave_result,
        "referral_anomalies": referral_result,
    }