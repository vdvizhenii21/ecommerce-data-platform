"""Assertions for raw ingestion, executed after each load."""

def check():
    import psycopg
    from src.config import connection_kwargs
    with psycopg.connect(**connection_kwargs()) as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT order_id), COUNT(*) FILTER (WHERE quantity <= 0 OR unit_price < 0) FROM raw.orders")
        total, distinct, bad = cur.fetchone()
        if total == 0 or total != distinct or bad:
            raise RuntimeError(f"Raw DQ failed: rows={total}, unique={distinct}, invalid={bad}")
    return total

if __name__ == "__main__":
    print(f"Raw quality checks OK: {check()} orders")
