from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ai_prediction import AIPrediction
from app.models.attendance import Attendance
from app.services.attendance_ai_features_service import (
    get_attendance_ai_features,
)
from app.services.attendance_ml_prediction_service import (
    predict_attendance_status,
)


def ai_prediction_service(db: Session, user_id: int):
    # Extract attendance features.
    features = get_attendance_ai_features(
        db=db,
        user_id=user_id,
    )

    # Handle users without attendance records.
    if features["total_records"] == 0:
        result = {
            "prediction": "No Data",
            "confidence": 0.0,
        }

        prediction_record = AIPrediction(
            user_id=user_id,
            prediction=result["prediction"],
            confidence=result["confidence"],
            prediction_date=datetime.now(),
            model_name="Random Forest - Synthetic Test Model",
        )

        db.add(prediction_record)
        db.commit()
        db.refresh(prediction_record)

        return result

    # Use the latest attendance record for ML prediction.
    latest_record = (
    db.query(Attendance)
    .filter(Attendance.user_id == user_id)
    .order_by(Attendance.date.desc())
    .first()
)

    if latest_record is None:
        return {
            "prediction": "No Data",
            "confidence": 0.0,
        }

    # Calculate day of week.
    day_of_week = latest_record.date.weekday()

    # Convert check-in time to minutes.
    check_in_minutes = None
    if latest_record.check_in is not None:
        check_in_minutes = (
            latest_record.check_in.hour * 60
            + latest_record.check_in.minute
        )

    # Convert check-out time to minutes.
    check_out_minutes = None
    if latest_record.check_out is not None:
        check_out_minutes = (
            latest_record.check_out.hour * 60
            + latest_record.check_out.minute
        )

    # Run ML prediction.
    ml_result = predict_attendance_status(
        day_of_week=day_of_week,
        check_in_minutes=check_in_minutes,
        check_out_minutes=check_out_minutes,
    )

    result = {
        "prediction": ml_result["prediction"],
        "confidence": ml_result["confidence"],
    }

    # Save prediction to database.
    prediction_record = AIPrediction(
        user_id=user_id,
        prediction=result["prediction"],
        confidence=result["confidence"],
        prediction_date=datetime.now(),
        model_name="Random Forest - Synthetic Test Model",
    )

    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return result