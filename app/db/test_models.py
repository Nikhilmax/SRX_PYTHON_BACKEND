import pytest
from .models import OrderStatus

# app/db/test_models.py

def test_order_status_enum_members():
    assert hasattr(OrderStatus, "pending")
    assert hasattr(OrderStatus, "processing")
    assert hasattr(OrderStatus, "completed")
    assert hasattr(OrderStatus, "cancelled")

def test_order_status_enum_values():
    assert OrderStatus.pending.value == "pending"
    assert OrderStatus.processing.value == "processing"
    assert OrderStatus.completed.value == "completed"
    assert OrderStatus.cancelled.value == "cancelled"

@pytest.mark.parametrize("status_str, expected_enum", [
    ("pending", OrderStatus.pending),
    ("processing", OrderStatus.processing),
    ("completed", OrderStatus.completed),
    ("cancelled", OrderStatus.cancelled),
])
def test_order_status_from_string(status_str, expected_enum):
    assert OrderStatus(status_str) == expected_enum

def test_order_status_invalid_value():
    with pytest.raises(ValueError):
        OrderStatus("not_a_status")