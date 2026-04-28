from src.platform_core.validation import has_required_columns


def test_has_required_columns_true():
    row = {"a": 1, "b": 2, "c": 3}
    assert has_required_columns(row, {"a", "b"})


def test_has_required_columns_false():
    row = {"a": 1}
    assert not has_required_columns(row, {"a", "b"})
