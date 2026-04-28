from dataclasses import asdict, dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class CustomerEvent:
    event_id: int
    customer_id: int
    event_type: str
    amount: float
    event_date: str


def build_dummy_rows(n: int = 25) -> list[dict]:
    if n <= 0:
        return []

    event_types = ["signup", "purchase", "renewal", "support"]
    base_date = date(2026, 1, 1)

    rows: list[dict] = []
    for i in range(1, n + 1):
        rows.append(
            asdict(
                CustomerEvent(
                    event_id=i,
                    customer_id=1000 + i,
                    event_type=event_types[(i - 1) % len(event_types)],
                    amount=round(10.5 * i, 2),
                    event_date=(base_date + timedelta(days=i - 1)).isoformat(),
                )
            )
        )
    return rows
