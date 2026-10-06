
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
    employee_id: int,
):
    # 1. Verify that the employee exists
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None

    # 2. Find the linked user by matching email
    user = (
        db.query(User)
        .filter(User.email == employee.email)
        .first()
    )

    # 3. Get attendance anomalies for this user only
    attendance_anomalies = []

    if user:
        attendance_result = get_anomalies(
            db=db,
            user_id=user.id,
        )

        attendance_anomalies = attendance_result.get(
            "anomalies", []
        )

    # 4. Detect leave anomalies
    leave_result = detect_leave_anomalies(
        db=db,
        employee_id=employee_id,
    )

    # 5. Detect referral anomalies
    referral_result = detect_referral_anomalies(
        db=db,
        employee_id=employee_id,
    )

    # 6. Calculate the combined anomaly count
    total_anomalies = (
        len(attendance_anomalies)
        + (
            1
            if leave_result["anomaly_detected"]
            else 0
        )
        + (
            1
            if referral_result["anomaly_detected"]
            else 0
        )
    )

    # 7. Return the combined results
    return {
        "employee_id": employee_id,
        "total_anomalies": total_anomalies,
        "attendance_anomalies": attendance_anomalies,
        "leave_anomalies": leave_result,
        "referral_anomalies": referral_result,
    }
