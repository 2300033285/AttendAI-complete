from sqlalchemy.orm import Session

from app.models.leave import Leave


def detect_leave_anomalies(
    db: Session,
    employee_id: int,
):
    # Get all approved leaves for the employee
    leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Approved",
        )
        .order_by(Leave.start_date)
        .all()
    )

    anomalies = []
    anomaly_score = 0

    # No approved leaves
    if not leaves:
        return {
            "employee_id": employee_id,
            "anomaly_detected": False,
            "anomaly_score": 0,
            "severity": "Normal",
            "total_leave_days": 0,
            "total_approved_leaves": 0,
            "short_leave_count": 0,
            "anomalies": [],
        }

    # ---------------------------------------------------------
    # Calculate total approved leave days
    # ---------------------------------------------------------
    total_leave_days = sum(
        (leave.end_date - leave.start_date).days + 1
        for leave in leaves
    )

    # ---------------------------------------------------------
    # Rule 1: Excessive total leave days
    # ---------------------------------------------------------
    if total_leave_days > 30:
        anomalies.append({
            "type": "Excessive Leave",
            "message": (
                "Employee has taken more than 30 approved "
                "leave days."
            )
        })

        anomaly_score += 30

    # ---------------------------------------------------------
    # Rule 2: Frequent leave requests
    # ---------------------------------------------------------
    total_approved_leaves = len(leaves)

    if total_approved_leaves > 10:
        anomalies.append({
            "type": "Frequent Leave Requests",
            "message": (
                "Employee has more than 10 approved "
                "leave requests."
            )
        })

        anomaly_score += 20

    # ---------------------------------------------------------
    # Rule 3: Repeated short-duration leaves
    # ---------------------------------------------------------
    short_leaves = 0

    for leave in leaves:
        leave_days = (
            leave.end_date - leave.start_date
        ).days + 1

        if leave_days <= 1:
            short_leaves += 1

    if short_leaves >= 5:
        anomalies.append({
            "type": "Repeated Short Leaves",
            "message": (
                "Employee has taken 5 or more "
                "single-day leaves."
            )
        })

        anomaly_score += 20

    # ---------------------------------------------------------
    # Rule 4: Unusual leave pattern
    # ---------------------------------------------------------
    unusual_pattern = False

    for i in range(1, len(leaves)):
        previous_leave = leaves[i - 1]
        current_leave = leaves[i]

        gap = (
            current_leave.start_date
            - previous_leave.end_date
        ).days

        if gap <= 2:
            unusual_pattern = True
            break

    if unusual_pattern:
        anomalies.append({
            "type": "Unusual Leave Pattern",
            "message": (
                "Multiple leave periods occur "
                "within a short gap."
            )
        })

        anomaly_score += 30

    # ---------------------------------------------------------
    # Determine severity
    # ---------------------------------------------------------
    if anomaly_score >= 60:
        severity = "High"
    elif anomaly_score >= 30:
        severity = "Medium"
    elif anomaly_score > 0:
        severity = "Low"
    else:
        severity = "Normal"

    # ---------------------------------------------------------
    # Return anomaly analysis
    # ---------------------------------------------------------
    return {
        "employee_id": employee_id,
        "anomaly_detected": len(anomalies) > 0,
        "anomaly_score": anomaly_score,
        "severity": severity,
        "total_leave_days": total_leave_days,
        "total_approved_leaves": total_approved_leaves,
        "short_leave_count": short_leaves,
        "anomalies": anomalies,
    }