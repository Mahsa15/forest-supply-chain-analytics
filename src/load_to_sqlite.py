import sqlite3
import pandas as pd

DB_PATH = "forest.db"

def load_csv(conn, table, path):
    df = pd.read_csv(path)
    df.to_sql(table, conn, if_exists="append", index=False)

def main():
    conn = sqlite3.connect(DB_PATH)

    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    load_csv(conn, "mills", "data/mills.csv")
    load_csv(conn, "stands", "data/stands.csv")
    load_csv(conn, "harvest_schedule", "data/harvest_schedule.csv")
    load_csv(conn, "deliveries", "data/deliveries.csv")

    conn.commit()
    conn.close()
    print(f"✅ Created and loaded SQLite DB: {DB_PATH}")

if __name__ == "__main__":
    main()
