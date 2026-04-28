from src.platform_core.config import AppConfig


def test_config_dataclass_fields():
    cfg = AppConfig(catalog="main", schema="test", table_name="tbl")
    assert cfg.catalog == "main"
    assert cfg.schema == "test"
    assert cfg.table_name == "tbl"
