-- sql/schema.sql
DROP TABLE IF EXISTS mills;
DROP TABLE IF EXISTS stands;
DROP TABLE IF EXISTS harvest_schedule;
DROP TABLE IF EXISTS deliveries;

CREATE TABLE mills (
  mill_id INTEGER PRIMARY KEY,
  mill_name TEXT NOT NULL,
  city TEXT NOT NULL,
  capacity_tons_week INTEGER NOT NULL
);

CREATE TABLE stands (
  stand_id INTEGER PRIMARY KEY,
  region TEXT NOT NULL,
  species TEXT NOT NULL,
  area_ha REAL NOT NULL,
  est_volume_tons INTEGER NOT NULL,
  risk_score REAL NOT NULL
);

CREATE TABLE harvest_schedule (
  week_start TEXT NOT NULL,
  stand_id INTEGER NOT NULL,
  planned_tons INTEGER NOT NULL,
  FOREIGN KEY (stand_id) REFERENCES stands(stand_id)
);

CREATE TABLE deliveries (
  week_start TEXT NOT NULL,
  stand_id INTEGER NOT NULL,
  mill_id INTEGER NOT NULL,
  actual_tons INTEGER NOT NULL,
  shipment_cost REAL NOT NULL,
  shipment_revenue REAL NOT NULL,
  FOREIGN KEY (stand_id) REFERENCES stands(stand_id),
  FOREIGN KEY (mill_id) REFERENCES mills(mill_id)
);
