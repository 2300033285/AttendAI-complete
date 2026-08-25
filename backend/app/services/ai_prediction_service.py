from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.ai_prediction import get_ai_prediction
from app.models.ai_prediction import AIPrediction


def ai_prediction_service(db: Session, user_id: int):

    # Calculate prediction
    result = get_ai_prediction(
        db=db,
        user_id=user_id
    )

    # Save prediction in database
    prediction_record = AIPrediction(
        user_id=user_id,
        prediction=result["prediction"],
        confidence=result["confidence"],
        prediction_date=datetime.now(),
        model_name="Attendance Model"
    )

    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    # Return API response
    return result