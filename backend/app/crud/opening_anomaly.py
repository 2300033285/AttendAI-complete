from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.opening import Opening


def get_opening_anomalies(db: Session):

    openings = db.query(Opening).all()

    results = []

    for opening in openings:

        anomalies = []
        severity = "Normal"

        # Rule 1: Open for more than 30 days
        if opening.status.lower() == "open":

            created_at = opening.created_at

            if created_at is not None:

                if created_at.tzinfo is None:
                    created_at = created_at.replace(
                        tzinfo=timezone.utc
                    )

                current_time = datetime.now(timezone.utc)

                open_days = (
                    current_time - created_at
                ).days

                if open_days > 30:
                    anomalies.append(
                        f"Opening has been active for {open_days} days"
                    )
                    severity = "Medium"

        # Rule 2: Missing job title
        if not opening.job_title or not opening.job_title.strip():
            anomalies.append(
                "Job title is missing"
            )
            severity = "High"

        # Rule 3: Missing department
        if not opening.department or not opening.department.strip():
            anomalies.append(
                "Department is missing"
            )
            severity = "High"

        # Rule 4: Missing location
        if not opening.location or not opening.location.strip():
            anomalies.append(
                "Location is missing"
            )
            severity = "Medium"

        results.append(
            {
                "opening_id": opening.id,
                "job_title": opening.job_title,
                "status": opening.status,
                "anomaly_detected": len(anomalies) > 0,
                "severity": severity,
                "anomalies": anomalies,
            }
        )

    return results