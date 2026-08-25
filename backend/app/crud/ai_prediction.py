from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def get_ai_prediction(db: Session, user_id: int):

    records = (
        db.query(Attendance)
        .filter(Attendance.user_id == user_id)
        .all()
    )

    if not records:
        return {
            "prediction": "No Data",
            "confidence": 0
        }

    total = len(records)

    present = sum(
        1
        for record in records
        if record.status and record.status.lower() == "present"
    )

    percentage = (present / total) * 100

    if percentage >= 90:
        prediction = "Excellent Attendance"

    elif percentage >= 75:
        prediction = "Good Attendance"

    elif percentage >= 50:
        prediction = "Average Attendance"

    else:
        prediction = "Poor Attendance"

    return {
        "prediction": prediction,
        "confidence": round(percentage, 2)
    }