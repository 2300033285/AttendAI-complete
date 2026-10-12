from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(__file__).resolve().parents[2] / "attendance_status_model.joblib"


def load_attendance_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Attendance model not found: {MODEL_PATH}"
        )

    saved_model = joblib.load(MODEL_PATH)

    return (
        saved_model["model"],
        saved_model["features"],
        saved_model["dataset_type"],
    )


def predict_attendance_status(
    day_of_week: int,
    check_in_minutes: float | None,
    check_out_minutes: float | None,
):
    model, features, dataset_type = load_attendance_model()

    input_data = pd.DataFrame(
        [
            {
                "day_of_week": day_of_week,
                "check_in_minutes": (
                    check_in_minutes if check_in_minutes is not None else -1
                ),
                "check_out_minutes": (
                    check_out_minutes if check_out_minutes is not None else -1
                ),
            }
        ]
    )

    input_data = input_data[features]

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    confidence = float(max(probabilities) * 100)

    return {
        "prediction": str(prediction),
        "confidence": round(confidence, 2),
        "model": "Random Forest",
        "dataset_type": dataset_type,
    }