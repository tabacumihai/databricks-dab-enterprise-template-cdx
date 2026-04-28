# Databricks notebook source
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "dab_template")
dbutils.widgets.text("table_name", "customer_events")
dbutils.widgets.text("row_count", "25")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
table_name = dbutils.widgets.get("table_name")
row_count = int(dbutils.widgets.get("row_count"))

from pyspark.sql import functions as F
from src.platform_core.dummy_data import build_dummy_rows

full_table = f"{catalog}.{schema}.{table_name}"

rows = build_dummy_rows(row_count)
df = spark.createDataFrame(rows).withColumn("event_date", F.to_date("event_date"))

spark.sql(f"DELETE FROM {full_table}")

(
    df.withColumn("inserted_at", F.current_timestamp())
      .write
      .mode("append")
      .saveAsTable(full_table)
)

display(spark.sql(f"SELECT * FROM {full_table} ORDER BY event_id"))
