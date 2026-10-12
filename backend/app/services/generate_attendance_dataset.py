
import pandas as pd
import random
from datetime import date, time, timedelta
from pathlib import Path

random.seed(42)

records = []
start_date = date(2025, 1, 1)

# Synthetic data for development and testing only
for user_id in range(1, 21):
    for day in range(100):
        attendance_date = start_date + timedelta(days=day)

        # Skip weekends
        if attendance_date.weekday() >= 5:
            continue

        status = random.choices(
            ["Present", "Late", "Absent"],
            weights=[75, 15, 10],
            k=1,
        )[0]

        if status == "Absent":
            check_in = None
            check_out = None
        else:
            if status == "Late":
                check_in = time(
                    9, random.randint(10, 45)
                ).strftime("%H:%M:%S")
            else:
                check_in = time(
                    8, random.randint(45, 59)
                ).strftime("%H:%M:%S")

            check_out = time(
                17, random.randint(0, 59)
            ).strftime("%H:%M:%S")

        records.append({
            "user_id": user_id,
            "date": attendance_date.isoformat(),
            "check_in": check_in,
            "check_out": check_out,
            "status": status,
            "dataset_type": "SYNTHETIC",
        })

df = pd.DataFrame(records)

output_path = (
    Path(__file__).resolve().parents[2]
    / "synthetic_attendance_dataset.csv"
)
df.to_csv(output_path, index=False)

print("Synthetic dataset created successfully.")
print("Records:", len(df))
print("Output:", output_path)
print(df["status"].value_counts())
