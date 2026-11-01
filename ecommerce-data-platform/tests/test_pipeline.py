import csv
from decimal import Decimal
import pytest
from src.generate_data import generate
from src.load import validate

def test_generator_is_deterministic(tmp_path):
    first = generate(15, tmp_path / "a.csv", 22)
    second = generate(15, tmp_path / "b.csv", 22)
    assert first.read_bytes() == second.read_bytes()
    with first.open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 15
    assert len({r["order_id"] for r in rows}) == 15

def test_valid_row():
    row = dict(order_id="O1", customer_id="C1", ordered_at="2026-01-01T00:00:00+00:00", category="books", quantity="2", unit_price="12.50", status="completed")
    assert validate(row)[5] == Decimal("12.50")

@pytest.mark.parametrize("field,value", [("quantity","0"),("unit_price","-1"),("status","unknown"),("ordered_at","bad")])
def test_reject_bad_data(field, value):
    row = dict(order_id="O1", customer_id="C1", ordered_at="2026-01-01T00:00:00+00:00", category="books", quantity="2", unit_price="12.50", status="completed")
    row[field] = value
    with pytest.raises(ValueError):
        validate(row)
