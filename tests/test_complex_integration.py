import pytest
from src.manager import Manager
from src.models import Parameters
from src.models import Bill


import pytest
from src.manager import Manager
from src.models import Parameters, Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0
    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 0.0
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0
    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 2622.0


def test_invalid_month():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='A1',
        date_due='2024-01-01',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=100,
        type='rent'
    ))

    with pytest.raises(ValueError):
        manager.get_apartment_costs('A1', 2024, 0)

    with pytest.raises(ValueError):
        manager.get_apartment_costs('A1', 2024, 13)