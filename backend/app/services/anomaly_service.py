from sqlalchemy.orm import Session

from app.crud.qr_anomaly import get_qr_anomalies


def anomaly_service(db: Session):
    return get_qr_anomalies(db)