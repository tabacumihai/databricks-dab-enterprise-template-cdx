CREATE OR REFRESH MATERIALIZED VIEW customer_events_mv
AS
SELECT
  event_id,
  customer_id,
  event_type,
  amount,
  event_date,
  inserted_at
FROM ${source_catalog}.${source_schema}.${source_table};

CREATE OR REFRESH MATERIALIZED VIEW customer_events_daily_mv
AS
SELECT
  event_date,
  event_type,
  COUNT(*) AS row_count,
  ROUND(SUM(amount), 2) AS total_amount
FROM customer_events_mv
GROUP BY event_date, event_type;
