def has_required_columns(row: dict, required_columns: set[str]) -> bool:
    return required_columns.issubset(set(row.keys()))
