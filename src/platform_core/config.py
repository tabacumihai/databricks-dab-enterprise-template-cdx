from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    catalog: str
    schema: str
    table_name: str


def load_config() -> AppConfig:
    return AppConfig(
        catalog=os.getenv("CATALOG", "main"),
        schema=os.getenv("SCHEMA", "dab_template"),
        table_name=os.getenv("TABLE_NAME", "customer_events"),
    )
