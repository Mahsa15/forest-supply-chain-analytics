-- 1) Weekly total planned vs actual
SELECT d.week_start,
       SUM(h.planned_tons) AS planned_tons,
       SUM(d.actual_tons)  AS actual_tons,
       ROUND(1.0 * SUM(d.actual_tons) / NULLIF(SUM(h.planned_tons), 0), 3) AS fulfillment
FROM harvest_schedule h
JOIN deliveries d ON d.week_start = h.week_start AND d.stand_id = h.stand_id
GROUP BY d.week_start
ORDER BY d.week_start;

-- 2) Mill utilization (actual / capacity)
SELECT d.week_start, m.mill_name,
       SUM(d.actual_tons) AS actual_tons,
       m.capacity_tons_week,
       ROUND(1.0 * SUM(d.actual_tons) / m.capacity_tons_week, 3) AS utilization
FROM deliveries d
JOIN mills m ON m.mill_id = d.mill_id
GROUP BY d.week_start, m.mill_name
ORDER BY d.week_start, utilization DESC;

-- 3) Profit by mill
SELECT m.mill_name,
       ROUND(SUM(d.shipment_revenue) - SUM(d.shipment_cost), 2) AS profit
FROM deliveries d
JOIN mills m ON m.mill_id = d.mill_id
GROUP BY m.mill_name
ORDER BY profit DESC;

-- 4) Profit by region
SELECT s.region,
       ROUND(SUM(d.shipment_revenue) - SUM(d.shipment_cost), 2) AS profit
FROM deliveries d
JOIN stands s ON s.stand_id = d.stand_id
GROUP BY s.region
ORDER BY profit DESC;

-- 5) Species mix delivered
SELECT s.species, SUM(d.actual_tons) AS tons
FROM deliveries d
JOIN stands s ON s.stand_id = d.stand_id
GROUP BY s.species
ORDER BY tons DESC;

-- 6) High-risk stands delivered (risk_score >= 0.75)
SELECT d.week_start, d.stand_id, s.region, s.species, s.risk_score, d.actual_tons
FROM deliveries d
JOIN stands s ON s.stand_id = d.stand_id
WHERE s.risk_score >= 0.75
ORDER BY s.risk_score DESC, d.actual_tons DESC
LIMIT 30;

-- 7) Biggest under-fulfillment weeks (actual < planned)
SELECT d.week_start,
       SUM(h.planned_tons) AS planned,
       SUM(d.actual_tons) AS actual,
       (SUM(h.planned_tons) - SUM(d.actual_tons)) AS gap
FROM harvest_schedule h
JOIN deliveries d ON d.week_start = h.week_start AND d.stand_id = h.stand_id
GROUP BY d.week_start
HAVING gap > 0
ORDER BY gap DESC
LIMIT 10;

-- 8) Cost per ton by mill
SELECT m.mill_name,
       ROUND(SUM(d.shipment_cost) / NULLIF(SUM(d.actual_tons),0), 2) AS cost_per_ton
FROM deliveries d
JOIN mills m ON m.mill_id = d.mill_id
GROUP BY m.mill_name
ORDER BY cost_per_ton ASC;

-- 9) Top stands by delivered volume
SELECT d.stand_id, SUM(d.actual_tons) AS total_tons
FROM deliveries d
GROUP BY d.stand_id
ORDER BY total_tons DESC
LIMIT 10;

-- 10) Data quality check: any negative or zero actual_tons?
SELECT COUNT(*) AS bad_rows
FROM deliveries
WHERE actual_tons <= 0;
