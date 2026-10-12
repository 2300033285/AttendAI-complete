
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "synthetic_attendance_dataset.csv"
MODEL_PATH = BASE_DIR / "attendance_status_model.joblib"

# Load the synthetic dataset
df = pd.read_csv(CSV_PATH)

# Extract useful features
df["date"] = pd.to_datetime(df["date"])
df["day_of_week"] = df["date"].dt.dayofweek

df["check_in_minutes"] = (
    pd.to_datetime(df["check_in"], format="%H:%M:%S", errors="coerce")
    .dt.hour * 60
    + pd.to_datetime(
        df["check_in"], format="%H:%M:%S", errors="coerce"
    ).dt.minute
)

df["check_out_minutes"] = (
    pd.to_datetime(df["check_out"], format="%H:%M:%S", errors="coerce")
    .dt.hour * 60
    + pd.to_datetime(
        df["check_out"], format="%H:%M:%S", errors="coerce"
    ).dt.minute
)

# Missing times are represented by -1
df[["check_in_minutes", "check_out_minutes"]] = (
    df[["check_in_minutes", "check_out_minutes"]].fillna(-1)
)

features = [
    "day_of_week",
    "check_in_minutes",
    "check_out_minutes",
]

X = df[features]
y = df["status"]

# Keep all status categories represented in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Dataset: SYNTHETIC — development testing only")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Test accuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save the trained test model
joblib.dump(
    {"model": model, "features": features, "dataset_type": "SYNTHETIC"},
    MODEL_PATH,
)

print("\nTest model saved to:", MODEL_PATH)
