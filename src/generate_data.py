"""Generate deterministic, synthetic e-commerce events. No customer PII."""
import csv
import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

CATEGORIES = ["electronics", "home", "fitness", "books", "beauty"]
STATUSES = ["completed", "completed", "completed", "cancelled", "returned"]

def generate(rows=1000, output="data/orders.csv", seed=42):
    if rows < 1:
        raise ValueError("rows must be positive")
    rng = random.Random(seed)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["order_id", "customer_id", "ordered_at", "category", "quantity", "unit_price", "status"])
        writer.writeheader()
        for n in range(1, rows + 1):
            writer.writerow({
                "order_id": f"ORD-{n:06d}",
                "customer_id": f"CUST-{rng.randint(1, 200):04d}",
                "ordered_at": (base + timedelta(hours=rng.randint(0, 24 * 180))).isoformat(),
                "category": rng.choice(CATEGORIES),
                "quantity": rng.randint(1, 4),
                "unit_price": f"{rng.uniform(5, 400):.2f}",
                "status": rng.choice(STATUSES),
            })
    return path

if __name__ == "__main__":
    path = generate(rows=int(os.getenv("ORDER_ROWS", "1000")), seed=int(os.getenv("SOURCE_SEED", "42")))
    print(f"Generated {path}")
