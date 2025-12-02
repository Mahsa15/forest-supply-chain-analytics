# src/generate_data.py
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

def daterange(start, end, step_days=7):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=step_days)

def main():
    # Mills
    mills = pd.DataFrame([
        {"mill_id": 1, "mill_name": "Maple Mill", "city": "Fredericton", "capacity_tons_week": 2200},
        {"mill_id": 2, "mill_name": "Pine Mill", "city": "Moncton", "capacity_tons_week": 1800},
        {"mill_id": 3, "mill_name": "Cedar Mill", "city": "Saint John", "capacity_tons_week": 2000},
    ])

    # Stands (harvest blocks)
    species = ["Spruce", "Pine", "Fir", "Hardwood"]
    stands = []
    for stand_id in range(1, 61):
        stands.append({
            "stand_id": stand_id,
            "region": random.choice(["North", "South", "East", "West"]),
            "species": random.choice(species),
            "area_ha": round(random.uniform(8, 45), 1),
            "est_volume_tons": int(random.uniform(400, 3500)),
            "risk_score": round(random.uniform(0, 1), 2)
        })
    stands = pd.DataFrame(stands)

    # Harvest schedule (weekly plan)
    start = date(2025, 1, 1)
    end = date(2025, 12, 31)

    schedule_rows = []
    for d in daterange(start, end, step_days=7):
        for _ in range(random.randint(3, 7)):  # 3-7 harvests per week
            stand_id = random.randint(1, 60)
            planned = int(random.uniform(150, 900))
            schedule_rows.append({
                "week_start": d.isoformat(),
                "stand_id": stand_id,
                "planned_tons": planned
            })
    harvest_schedule = pd.DataFrame(schedule_rows)

    # Deliveries (actual shipments to mills)
    deliveries_rows = []
    for _, row in harvest_schedule.iterrows():
        # actual can deviate
        actual = max(0, int(row["planned_tons"] * random.uniform(0.7, 1.2)))
        mill_id = random.choice([1, 2, 3])
        cost = round(actual * random.uniform(8.0, 16.0), 2)      # transport + ops cost
        revenue = round(actual * random.uniform(18.0, 28.0), 2)  # selling price basis
        deliveries_rows.append({
            "week_start": row["week_start"],
            "stand_id": row["stand_id"],
            "mill_id": mill_id,
            "actual_tons": actual,
            "shipment_cost": cost,
            "shipment_revenue": revenue
        })
    deliveries = pd.DataFrame(deliveries_rows)

    # Save
    import os
    os.makedirs("data", exist_ok=True)
    mills.to_csv("data/mills.csv", index=False)
    stands.to_csv("data/stands.csv", index=False)
    harvest_schedule.to_csv("data/harvest_schedule.csv", index=False)
    deliveries.to_csv("data/deliveries.csv", index=False)

    print("✅ CSV files generated in /data")

if __name__ == "__main__":
    main()
