from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.qr_attendance import QRAttendance


def get_qr_anomalies(db: Session):

    records = (
        db.query(
            QRAttendance.employee_id,
            func.count(QRAttendance.id).label("total_scans")
        )
        .group_by(QRAttendance.employee_id)
        .all()
    )

    results = []

    for employee_id, total_scans in records:

        if total_scans > 5:
            results.append({
                "employee_id": employee_id,
                "total_scans": total_scans,
                "anomaly": True,
                "reason": "Unusually high number of QR scans"
            })

        else:
            results.append({
                "employee_id": employee_id,
                "total_scans": total_scans,
                "anomaly": False,
                "reason": "Normal QR attendance activity"
            })

    return results