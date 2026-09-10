from sqlalchemy.orm import Session

from app.services.leave_analytics_service import (
    get_leave_summary_service,
    get_leave_days_summary_service,
)

from app.services.leave_anomaly_service import (
    detect_leave_anomalies,
)


def get_leave_insights_service(
    db: Session,
    employee_id: int,
):
    # ---------------------------------------------------------
    # 1. Get leave summary
    # ---------------------------------------------------------
    summary = get_leave_summary_service(
        db=db,
        employee_id=employee_id,
    )

    # ---------------------------------------------------------
    # 2. Get total leave days
    # ---------------------------------------------------------
    days_result = get_leave_days_summary_service(
        db=db,
        employee_id=employee_id,
    )

    total_leave_days = 0

    if days_result:
        total_leave_days = (
            days_result[0].get("total_leave_days", 0) or 0
        )

    # ---------------------------------------------------------
    # 3. Get anomaly information
    # ---------------------------------------------------------
    anomaly_result = detect_leave_anomalies(
        db=db,
        employee_id=employee_id,
    )

    # ---------------------------------------------------------
    # 4. Calculate average leave duration
    # ---------------------------------------------------------
    total_leave_requests = summary.get(
        "total_leaves", 0
    )

    if total_leave_requests > 0:
        average_leave_duration = round(
            total_leave_days / total_leave_requests,
            2,
        )
    else:
        average_leave_duration = 0

    # ---------------------------------------------------------
    # 5. Prepare insights
    # ---------------------------------------------------------
    insights = []

    # Leave usage insight
    if total_leave_days > 0:
        insights.append(
            f"Employee has taken {total_leave_days} total "
            f"leave days."
        )
    else:
        insights.append(
            "Employee has not used any leave days."
        )

    # Approved leaves insight
    approved_leaves = summary.get(
        "approved_leaves", 0
    )

    if approved_leaves > 0:
        insights.append(
            f"Employee has {approved_leaves} approved "
            f"leave requests."
        )

    # Rejected leaves insight
    rejected_leaves = summary.get(
        "rejected_leaves", 0
    )

    if rejected_leaves > 0:
        insights.append(
            f"Employee has {rejected_leaves} rejected "
            f"leave requests."
        )

    # Pending leaves insight
    pending_leaves = summary.get(
        "pending_leaves", 0
    )

    if pending_leaves > 0:
        insights.append(
            f"Employee has {pending_leaves} pending "
            f"leave requests."
        )

    # Average duration insight
    if average_leave_duration > 0:
        insights.append(
            f"Average leave duration is "
            f"{average_leave_duration} days per request."
        )

    # ---------------------------------------------------------
    # 6. Add anomaly insights
    # ---------------------------------------------------------
    if anomaly_result.get("anomaly_detected"):

        for anomaly in anomaly_result.get(
            "anomalies", []
        ):
            insights.append(
                anomaly["message"]
            )

    # ---------------------------------------------------------
    # 7. Determine recommendation
    # ---------------------------------------------------------
    anomaly_score = anomaly_result.get(
        "anomaly_score", 0
    )

    severity = anomaly_result.get(
        "severity", "Normal"
    )

    if severity == "High":
        recommendation = (
            "High-risk leave pattern detected. "
            "Review the employee's leave history."
        )

    elif severity == "Medium":
        recommendation = (
            "Moderate leave pattern detected. "
            "Monitor future leave activity."
        )

    elif severity == "Low":
        recommendation = (
            "Minor unusual leave activity detected. "
            "Continue monitoring the leave pattern."
        )

    else:
        recommendation = (
            "Leave usage appears normal. "
            "No immediate action is required."
        )

    # ---------------------------------------------------------
    # 8. Return complete leave insights
    # ---------------------------------------------------------
    return {
        "employee_id": employee_id,

        "total_leave_days": total_leave_days,

        "total_leave_requests": total_leave_requests,

        "approved_leaves": approved_leaves,

        "rejected_leaves": rejected_leaves,

        "pending_leaves": pending_leaves,

        "average_leave_duration": average_leave_duration,

        "anomaly_detected": anomaly_result.get(
            "anomaly_detected", False
        ),

        "anomaly_score": anomaly_score,

        "severity": severity,

        "anomalies": anomaly_result.get(
            "anomalies", []
        ),

        "insights": insights,

        "recommendation": recommendation,
    }