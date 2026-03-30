import pytest
from src.manager import Manager

class DummyBill:
    def __init__(self, year, month, amount):
        self.year = year
        self.month = month
        self.amount = amount
        
class DummyApartment:
    def __init__(self, bills=None):
        self.bills = bills or []
        
def test_get_apartment_cost_integration():
    manager = Manager()
    
    assert manager.get_apartment_costs("A1", 2024, 3) is None
    
    apt = DummyApartment(bills=[
        DummyBill(2024, 1, 100.0),
        DummyBill(2024, 1, 200.0),
    ])
    manager.add_apartment("A1", apt)
    
    assert manager.get_apartment_costs("A1", 2024, 3) == 0.0
    
    apt.bills.extend([
        DummyBill(2024, 3, 150.0),
        DummyBill(2024, 3, 200.0),
        DummyBill(2024, 3, 100.0),
    ])
    
    assert manager.get_apartment_costs("A1", 2024, 3) == 450.0
    
def test_invalid_month_raises_error():
    manager = Manager()
    apt = DummyApartment(bills=[])
    manager.add_apartment("A1", apt)
    
    try:
        manager.get_apartment_costs("A1", 2024, 0)
        assert False, "Expected ValueError for month=0"
    except ValueError:
        pass
    
    try:
        manager.get_apartment_costs("A1", 2024, 13)
        assert False, "Expected ValueError for month=13"
    except ValueError:
        pass
    
def test_sum_whole_history():
    manager = Manager()
    apt = DummyApartment(bills=[
        DummyBill(2023, 1, 100),
        DummyBill(2024, 5, 200),
        DummyBill(2024, 6, 300),
    ])
    manager.add_apartment("A1", apt)
    
    assert manager.get_apartment_costs("A1") == 600
    
def test_sum_year_only():
    manager = Manager()
    apt = DummyApartment(bills=[
        DummyBill(2024, 1, 100),
        DummyBill(2024, 2, 200),
        DummyBill(2024, 5, 300),
    ])
    manager.add_apartment("A1", apt)
    
    assert manager.get_apartment_costs ("A1", 2024) == 300
    
def test_sum_specific_month():
    manager = Manager()
    apt = DummyApartment(bills=[
        DummyBill(2024, 3, 150),
        DummyBill(2024, 3, 250),
        DummyBill(2024, 4, 100),
    ])
    manager.add_apartment("A1", apt)
    
    assert manager.get_apartment_costs ("A1", 2024, 3) == 400