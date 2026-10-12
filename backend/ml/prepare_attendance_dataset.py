
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
input_file = base_dir / "attendance_dataset.csv"
output_file = base_dir / "attendance_features.csv"

df = pd.read_csv(input_file)

# Normalize attendance status.
df["status"] = df["status"].astype("string").str.strip().str.lower()

# Convert dates and times.
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["check_in"] = pd.to_timedelta(
    df["check_in"].astype("string"), errors="coerce"
)
df["check_out"] = pd.to_timedelta(
    df["check_out"].astype("string"), errors="coerce"
)

# Create attendance features.
df["is_present"] = df["status"].isin(["present", "late"]).astype(int)
df["is_late"] = df["status"].eq("late").astype(int)
df["is_absent"] = df["status"].eq("absent").astype(int)

# Calculate working hours.
df["working_hours"] = (
    df["check_out"] - df["check_in"]
).dt.total_seconds() / 3600

# Handle overnight shifts.
df.loc[df["working_hours"] < 0, "working_hours"] += 24

# Missing times remain missing for absent records.
df["day_of_week"] = df["date"].dt.dayofweek

# Export prepared data.
df.to_csv(output_file, index=False)

print("Dataset preparation completed.")
print("Records:", len(df))
print("Saved to:", output_file)
print(df[[
    "user_id", "date", "status", "working_hours",
    "is_present", "is_late", "is_absent"
]].to_string(index=False))
