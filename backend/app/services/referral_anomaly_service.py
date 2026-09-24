from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.referral import Referral


def detect_referral_anomalies(
    db: Session,
    employee_id: int
):

    total_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.employee_id == employee_id)
        .scalar()
        or 0
    )

    pending_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Pending"
        )
        .scalar()
        or 0
    )

    rejected_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Rejected"
        )
        .scalar()
        or 0
    )

    anomalies = []
    anomaly_score = 0

    # Rule 1: Excessive referrals
    if total_referrals > 10:
        anomalies.append(
            "Employee has submitted an unusually high number of referrals."
        )
        anomaly_score += 1

    # Rule 2: Too many pending referrals
    if pending_referrals > 5:
        anomalies.append(
            "Employee has an unusually high number of pending referrals."
        )
        anomaly_score += 1

    # Rule 3: High rejection count
    if rejected_referrals > 5:
        anomalies.append(
            "Employee has an unusually high number of rejected referrals."
        )
        anomaly_score += 1

    if anomaly_score == 0:
        severity = "Normal"
        anomaly_detected = False
    elif anomaly_score == 1:
        severity = "Low"
        anomaly_detected = True
    elif anomaly_score == 2:
        severity = "Medium"
        anomaly_detected = True
    else:
        severity = "High"
        anomaly_detected = True

    return {
        "employee_id": employee_id,
        "anomaly_detected": anomaly_detected,
        "anomaly_score": anomaly_score,
        "severity": severity,
        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "rejected_referrals": rejected_referrals,
        "anomalies": anomalies
    }