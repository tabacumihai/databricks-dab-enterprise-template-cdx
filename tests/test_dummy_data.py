from src.platform_core.dummy_data import build_dummy_rows


def test_build_dummy_rows_count():
    rows = build_dummy_rows(3)
    assert len(rows) == 3


def test_build_dummy_rows_empty():
    assert build_dummy_rows(0) == []


def test_build_dummy_rows_columns():
    row = build_dummy_rows(1)[0]
    assert set(row.keys()) == {
        "event_id",
        "customer_id",
        "event_type",
        "amount",
        "event_date",
    }
