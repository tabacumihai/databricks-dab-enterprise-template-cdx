# Databricks notebook source
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "dab_template")
dbutils.widgets.text("table_name", "customer_events")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
table_name = dbutils.widgets.get("table_name")

full_table = f"{catalog}.{schema}.{table_name}"

row_count = spark.sql(f"SELECT COUNT(*) AS cnt FROM {full_table}").collect()[0]["cnt"]
null_ids = spark.sql(f"SELECT COUNT(*) AS cnt FROM {full_table} WHERE event_id IS NULL").collect()[0]["cnt"]

assert row_count > 0, f"{full_table} is empty"
assert null_ids == 0, f"{full_table} contains null event_id values"

print(f"Quality checks passed for {full_table}")
