"""Idempotent batch load with upsert and validation."""
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {"order_id", "customer_id", "ordered_at", "category", "quantity", "unit_price", "status"}
ALLOWED = {"completed", "cancelled", "returned"}

def validate(row):
    if not REQUIRED.issubset(row):
        raise ValueError("Missing required columns")
    if any(not row[k] for k in REQUIRED):
        raise ValueError(f"Missing required value for order {row.get('order_id')}")
    try:
        ts = datetime.fromisoformat(row["ordered_at"])
        qty = int(row["quantity"])
        price = Decimal(row["unit_price"])
    except (ValueError, InvalidOperation) as exc:
        raise ValueError(f"Invalid values for order {row['order_id']}") from exc
    if ts.tzinfo is None or qty <= 0 or not price.is_finite() or price < 0 or row["status"] not in ALLOWED:
        raise ValueError(f"Failed data quality checks for {row['order_id']}")
    return (row["order_id"], row["customer_id"], ts, row["category"], qty, price, row["status"])

def load(path="data/orders.csv"):
    sql_path = Path(__file__).resolve().parents[1] / "sql" / "001_init.sql"
    import psycopg
    from src.config import connection_kwargs
    with psycopg.connect(**connection_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_path.read_text())
            count = 0
            with Path(path).open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not REQUIRED.issubset(reader.fieldnames or []):
                    raise ValueError("CSV has missing columns")
                for row in reader:
                    cur.execute("""
                        INSERT INTO raw.orders (order_id,customer_id,ordered_at,category,quantity,unit_price,status)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (order_id) DO UPDATE SET
                          customer_id=EXCLUDED.customer_id,
                          ordered_at=EXCLUDED.ordered_at,
                          category=EXCLUDED.category,
                          quantity=EXCLUDED.quantity,
                          unit_price=EXCLUDED.unit_price,
                          status=EXCLUDED.status,
                          loaded_at=NOW()
                    """, validate(row))
                    count += 1
    return count

if __name__ == "__main__":
    print(f"Upserted {load()} orders")
