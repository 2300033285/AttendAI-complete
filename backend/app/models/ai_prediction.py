from sqlalchemy import Column, Integer, String, Numeric, DateTime
from app.database import Base


class AIPrediction(Base):

    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    prediction = Column(String, nullable=False)

    confidence = Column(Numeric, nullable=False)

    prediction_date = Column(DateTime, nullable=False)

    model_name = Column(String, nullable=False)