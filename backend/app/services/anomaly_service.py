from sqlalchemy.orm import Session

from app.crud.attendance_anomaly import get_anomalies


def anomaly_service(db: Session):
    return get_anomalies(db)