from sqlalchemy.orm import Session

from app.models.leave import Leave
from app.services.leave_anomaly_service import (
    detect_leave_anomalies,
)


def get_leave_ai_features(
    db: Session,
    employee_id: int,
):
    # Get all leave records for the employee
    leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id
        )
        .order_by(Leave.start_date)
        .all()
    )

    # ---------------------------------------------------------
    # No leave records
    # ---------------------------------------------------------
    if not leaves:
        return {
            "employee_id": employee_id,
            "total_leave_requests": 0,
            "approved_leave_count": 0,
            "rejected_leave_count": 0,
            "pending_leave_count": 0,
            "total_leave_days": 0,
            "average_leave_duration": 0,
            "short_leave_count": 0,
            "leave_type_counts": {},
            "anomaly_score": 0,
            "anomaly_severity": "Normal",
            "anomaly_detected": False,
        }

    # ---------------------------------------------------------
    # Count leave requests
    # ---------------------------------------------------------
    total_leave_requests = len(leaves)

    approved_leave_count = sum(
        1
        for leave in leaves
        if leave.status == "Approved"
    )

    rejected_leave_count = sum(
        1
        for leave in leaves
        if leave.status == "Rejected"
    )

    pending_leave_count = sum(
        1
        for leave in leaves
        if leave.status == "Pending"
    )

    # ---------------------------------------------------------
    # Calculate leave duration
    # ---------------------------------------------------------
    leave_durations = [
        (leave.end_date - leave.start_date).days + 1
        for leave in leaves
    ]

    total_leave_days = sum(leave_durations)

    average_leave_duration = round(
        total_leave_days / total_leave_requests,
        2,
    )

    # ---------------------------------------------------------
    # Count short leaves
    # ---------------------------------------------------------
    short_leave_count = sum(
        1
        for duration in leave_durations
        if duration <= 1
    )

    # ---------------------------------------------------------
    # Count leave types
    # ---------------------------------------------------------
    leave_type_counts = {}

    for leave in leaves:
        leave_type = leave.leave_type

        if leave_type not in leave_type_counts:
            leave_type_counts[leave_type] = 0

        leave_type_counts[leave_type] += 1

    # ---------------------------------------------------------
    # Get anomaly information
    # ---------------------------------------------------------
    anomaly_result = detect_leave_anomalies(
        db=db,
        employee_id=employee_id,
    )

    # ---------------------------------------------------------
    # Return AI-ready features
    # ---------------------------------------------------------
    return {
        "employee_id": employee_id,
        "total_leave_requests": total_leave_requests,
        "approved_leave_count": approved_leave_count,
        "rejected_leave_count": rejected_leave_count,
        "pending_leave_count": pending_leave_count,
        "total_leave_days": total_leave_days,
        "average_leave_duration": average_leave_duration,
        "short_leave_count": short_leave_count,
        "leave_type_counts": leave_type_counts,
        "anomaly_score": anomaly_result.get(
            "anomaly_score",
            0,
        ),
        "anomaly_severity": anomaly_result.get(
            "severity",
            "Normal",
        ),
        "anomaly_detected": anomaly_result.get(
            "anomaly_detected",
            False,
        ),
    }