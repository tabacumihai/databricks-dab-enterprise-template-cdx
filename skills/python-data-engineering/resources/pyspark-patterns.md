# PySpark Patterns and Optimization

## Table of Contents
1. [Job Structure](#job-structure)
2. [Performance Optimization](#performance-optimization)
3. [Join Strategies](#join-strategies)
4. [Window Functions](#window-functions)
5. [Partition Management](#partition-management)
6. [Error Handling](#error-handling)

## Job Structure

### Production PySpark Job Template

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging
from typing import Dict, Any
import sys

class ProductionSparkJob:
    """Base class for production PySpark jobs."""

    def __init__(self, job_name: str, config: Dict[str, Any]):
        self.config = config
        self.spark = self._create_spark_session(job_name)
        self.logger = self._setup_logging()

    def _create_spark_session(self, job_name: str) -> SparkSession:
        """Create optimized Spark session."""
        return (SparkSession.builder
            .appName(job_name)
            # Adaptive Query Execution
            .config("spark.sql.adaptive.enabled", "true")
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
            # Dynamic partition pruning
            .config("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
            # Broadcast join threshold
            .config("spark.sql.autoBroadcastJoinThreshold", "100MB")
            # S3 optimization
            .config("spark.hadoop.fs.s3a.connection.maximum", "100")
            .config("spark.hadoop.fs.s3a.threads.max", "50")
            # Parquet optimization
            .config("spark.sql.parquet.mergeSchema", "false")
            .config("spark.sql.parquet.filterPushdown", "true")
            .getOrCreate())

    def _setup_logging(self) -> logging.Logger:
        """Configure structured logging."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        return logger

    def run(self):
        """Main execution method - override in subclass."""
        raise NotImplementedError("Subclass must implement run()")

    def cleanup(self):
        """Cleanup resources."""
        self.spark.stop()
```

### Example ETL Job

```python
class BronzeToSilverETL(ProductionSparkJob):
    """Process raw data to cleaned silver zone."""

    def run(self):
        try:
            # Read bronze data
            df_bronze = self.read_bronze()

            # Transform
            df_silver = self.transform(df_bronze)

            # Data quality
            self.validate_quality(df_silver)

            # Write silver
            self.write_silver(df_silver)

            self.logger.info("ETL completed successfully")
        except Exception as e:
            self.logger.error(f"ETL failed: {e}")
            raise

    def read_bronze(self):
        """Read from bronze zone with schema."""
        schema = StructType([
            StructField("id", StringType(), False),
            StructField("timestamp", TimestampType(), False),
            StructField("value", DoubleType(), True),
            StructField("metadata", MapType(StringType(), StringType()), True)
        ])

        return (self.spark.read
            .schema(schema)
            .option("mode", "PERMISSIVE")
            .option("columnNameOfCorruptRecord", "_corrupt_record")
            .parquet(self.config['bronze_path']))

    def transform(self, df):
        """Clean and enrich data."""
        return (df
            # Filter corrupt records
            .filter(col("_corrupt_record").isNull())

            # Deduplicate
            .dropDuplicates(["id", "timestamp"])

            # Add processing metadata
            .withColumn("processed_at", current_timestamp())
            .withColumn("processing_date", current_date())

            # Extract nested fields
            .withColumn("source", col("metadata").getItem("source"))

            # Data validation
            .withColumn("is_valid",
                when((col("value").isNotNull()) &
                     (col("value") >= 0) &
                     (col("value") <= 1000), True)
                .otherwise(False))

            # Filter only valid
            .filter(col("is_valid"))
            .drop("is_valid", "_corrupt_record"))

    def validate_quality(self, df):
        """Data quality checks."""
        total_count = df.count()
        null_value_count = df.filter(col("value").isNull()).count()

        if total_count == 0:
            raise ValueError("No records after transformation")

        null_percentage = (null_value_count / total_count) * 100
        if null_percentage > 5:  # Max 5% nulls allowed
            raise ValueError(f"Null value percentage too high: {null_percentage}%")

        self.logger.info(f"Quality check passed: {total_count} records")

    def write_silver(self, df):
        """Write to silver zone with partitioning."""
        (df.write
            .mode("overwrite")
            .partitionBy("processing_date")
            .option("compression", "snappy")
            .parquet(self.config['silver_path']))
```

## Performance Optimization

### 1. Partition Optimization

```python
# Repartition for balanced workload
df_repartitioned = df.repartition(200)  # Based on cluster size

# Coalesce to reduce output files (no shuffle)
df_coalesced = df.coalesce(10)

# Repartition by column for downstream joins
df_partitioned = df.repartition("user_id")

# Dynamic partition based on data size
import math
data_size_gb = estimate_size_gb(df)
optimal_partitions = math.ceil(data_size_gb / 0.128)  # 128MB per partition
df_optimized = df.repartition(optimal_partitions)
```

### 2. Broadcast Joins

```python
from pyspark.sql.functions import broadcast

# Broadcast small dimension table (< 100MB)
df_large = spark.read.parquet("s3://large-dataset/")
df_small = spark.read.parquet("s3://dimension-table/")

# Explicit broadcast
df_joined = df_large.join(
    broadcast(df_small),
    on="dimension_id",
    how="left"
)

# Check if broadcast happened
df_joined.explain()  # Look for BroadcastHashJoin
```

### 3. Caching Strategy

```python
# Cache when DataFrame is reused multiple times
df_users = spark.read.parquet("s3://users/")

# Cache in memory
df_users.cache()

# Persist with storage level
from pyspark import StorageLevel
df_users.persist(StorageLevel.MEMORY_AND_DISK)

# Use cached data
df_active = df_users.filter(col("status") == "active")
df_premium = df_users.filter(col("tier") == "premium")

# Unpersist when done
df_users.unpersist()
```

## Join Strategies

### 1. Broadcast Hash Join (Small Table)

```python
# Best for: Small table (< 100MB) joining with large table
# No shuffle, very fast

df_result = df_large.join(
    broadcast(df_small),
    on="key",
    how="left"
)
```

### 2. Sort Merge Join (Large Tables)

```python
# Best for: Both tables are large and sorted
# Requires shuffle but efficient for large datasets

df_result = (
    df_large.repartition("user_id")
    .sortWithinPartitions("user_id")
    .join(
        df_events.repartition("user_id").sortWithinPartitions("user_id"),
        on="user_id",
        how="inner"
    )
)
```

### 3. Shuffle Hash Join

```python
# Spark chooses automatically based on data size
# Typically for medium-sized tables

df_result = df_table1.join(df_table2, on="key", how="inner")
```

### 4. Skewed Join Handling

```python
from pyspark.sql.functions import rand, concat, lit

# Add salt to skewed key
df_skewed_salted = df_skewed.withColumn(
    "salted_key",
    concat(col("key"), lit("_"), (rand() * 10).cast("int"))
)

# Replicate dimension table
df_dimension_replicated = df_dimension.withColumn(
    "salt",
    explode(array([lit(i) for i in range(10)]))
).withColumn(
    "salted_key",
    concat(col("key"), lit("_"), col("salt"))
)

# Join on salted key
df_result = df_skewed_salted.join(
    df_dimension_replicated,
    on="salted_key",
    how="left"
).drop("salted_key", "salt")
```

## Window Functions

### 1. Ranking and Row Number

```python
from pyspark.sql.window import Window

# Define window
window_spec = Window.partitionBy("user_id").orderBy(col("timestamp").desc())

# Rank, dense_rank, row_number
df_ranked = df.withColumn("rank", rank().over(window_spec))
df_dense = df.withColumn("dense_rank", dense_rank().over(window_spec))
df_numbered = df.withColumn("row_num", row_number().over(window_spec))

# Get latest record per user
df_latest = (df_numbered
    .filter(col("row_num") == 1)
    .drop("row_num"))
```

### 2. Aggregations in Window

```python
# Running totals
window_running = Window.partitionBy("user_id").orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)

df_cumulative = df.withColumn(
    "cumulative_amount",
    sum("amount").over(window_running)
)

# Moving average (7-day)
window_moving = Window.partitionBy("user_id").orderBy("date").rowsBetween(-6, 0)

df_moving_avg = df.withColumn(
    "moving_avg_7d",
    avg("value").over(window_moving)
)
```

### 3. Lead and Lag

```python
window_ordered = Window.partitionBy("user_id").orderBy("timestamp")

df_with_previous = df.withColumn(
    "previous_value",
    lag("value", 1).over(window_ordered)
).withColumn(
    "next_value",
    lead("value", 1).over(window_ordered)
).withColumn(
    "value_change",
    col("value") - col("previous_value")
)
```

## Partition Management

### 1. Writing Partitioned Data

```python
# Partition by date for time-series queries
df.write.partitionBy("year", "month", "day").parquet(output_path)

# Coalesce before write to control file count
(df
    .coalesce(10)  # 10 files per partition
    .write
    .partitionBy("date")
    .mode("overwrite")
    .parquet(output_path))

# Dynamic partitioning
df.write.option("partitionOverwriteMode", "dynamic").mode("overwrite").partitionBy("region").parquet(output_path)
```

### 2. Partition Pruning

```python
# Read with partition filter (pushed down, very fast)
df_filtered = (spark.read
    .parquet("s3://data/events/")
    .filter((col("year") == 2025) & (col("month") == 11)))

# Verify partition pruning
df_filtered.explain()  # Should see PartitionFilters
```

### 3. Bucket Optimization

```python
# Write bucketed data for efficient joins
(df_users
    .write
    .bucketBy(100, "user_id")
    .sortBy("user_id")
    .mode("overwrite")
    .saveAsTable("users_bucketed"))

# Join with another bucketed table (no shuffle!)
df_joined = spark.table("users_bucketed").join(
    spark.table("events_bucketed"),
    on="user_id"
)
```

## Error Handling

### 1. Corrupt Record Handling

```python
schema_with_corrupt = StructType([
    StructField("id", StringType()),
    StructField("value", IntegerType()),
    StructField("_corrupt_record", StringType())
])

df = (spark.read
    .schema(schema_with_corrupt)
    .option("mode", "PERMISSIVE")  # PERMISSIVE, DROPMALFORMED, or FAILFAST
    .option("columnNameOfCorruptRecord", "_corrupt_record")
    .json(input_path))

# Separate good and bad records
df_good = df.filter(col("_corrupt_record").isNull()).drop("_corrupt_record")
df_bad = df.filter(col("_corrupt_record").isNotNull())

# Write bad records to DLQ
df_bad.write.mode("append").parquet("s3://dlq/corrupt-records/")
```

### 2. Try-Catch in UDFs

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def safe_transform(value):
    try:
        # Risky transformation
        return complex_transformation(value)
    except Exception as e:
        # Log error
        logger.error(f"Transform failed: {e}")
        return None

df_transformed = df.withColumn("result", safe_transform(col("input")))
```

## Optimization Checklist

- Use appropriate join strategy based on table sizes
- Partition data aligned with query patterns
- Cache DataFrames when reused multiple times
- Use broadcast joins for small dimension tables
- Avoid UDFs when built-in functions available
- Filter data as early as possible
- Use columnar formats (Parquet, ORC)
- Enable adaptive query execution
- Monitor partition sizes (aim for 128MB-1GB)
- Use partition pruning in queries
- Avoid `collect()` on large datasets
- Use `explain()` to verify query plans

---

**Optimization Impact**: Following these patterns can improve performance by 5-10x
**Cost Savings**: Proper partitioning and join strategies reduce compute time by 50-70%