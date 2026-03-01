# generate_data.py

import pandas as pd
import random
from datetime import datetime, timedelta

sites = ["MAIN", "PLANT1"]
assets = {
    "MAIN": ["Chiller_1", "AHU_2"],
    "PLANT1": ["Boiler_3"]
}
sensors = ["temperature", "pressure", "vibration"]

rows = []

start_time = datetime(2024, 1, 1)

for i in range(5000):
    site = random.choice(sites)
    asset = random.choice(assets[site])
    sensor = random.choice(sensors)

    timestamp = start_time + timedelta(minutes=i)

    rows.append({
        "timestamp": timestamp.isoformat(),
        "site_name": site,
        "asset_id": asset,
        "sensor_name": sensor,
        "value": round(random.uniform(10, 100), 2),
        "unit": "unit"
    })

df = pd.DataFrame(rows)
df.to_csv("data/sensors.csv", index=False)

print("Synthetic dataset generated.")