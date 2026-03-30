import pytest
from src.manager import Manager
from src.models import Parameters, Bill, ApartmentSettlement, Tenant, TenantSettlement


def test_create_apartment_settlement_basic():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment="A1",
        date_due="2024-03-10",
        settlement_year=2024,
        settlement_month=3,
        amount_pln=300.0,
        type="rent"
    ))

    manager.bills.append(Bill(
        apartment="A1",
        date_due="2024-03-15",
        settlement_year=2024,
        settlement_month=3,
        amount_pln=150.0,
        type="electricity"
    ))

    manager.bills.append(Bill(
        apartment="A1",
        date_due="2024-02-10",
        settlement_year=2024,
        settlement_month=2,
        amount_pln=500.0,
        type="rent"
    ))

    settlement = manager.create_apartment_settlement("A1", 2024, 3)


    assert settlement is not None

    assert isinstance(settlement, ApartmentSettlement)

    assert settlement.apartment == "A1"

    assert settlement.year == 2024

    assert settlement.month == 3

    assert settlement.total_bills_pln == 450.0

    assert settlement.total_rent_pln == 0.0

    assert settlement.total_due_pln == 450.0

    assert settlement.total_bills_pln != 950.0

    empty_settlement = manager.create_apartment_settlement("A1", 2024, 1)
    assert empty_settlement.total_bills_pln == 0.0
    assert empty_settlement.total_due_pln == 0.0
    assert empty_settlement.total_rent_pln == 0.0
    
def test_create_tenant_settlements():
    manager = Manager(Parameters())

    manager.tenants = {
        key: tenant for key, tenant in manager.tenants.items()
        if tenant.apartment == "apart-polanka"
    }

    assert len(manager.tenants) == 3

    manager.bills.append(Bill(
        apartment="apart-polanka",
        date_due="2024-03-10",
        settlement_year=2024,
        settlement_month=3,
        amount_pln=600.0,
        type="rent"
    ))

    manager.bills.append(Bill(
        apartment="apart-polanka",
        date_due="2024-03-15",
        settlement_year=2024,
        settlement_month=3,
        amount_pln=300.0,
        type="electricity"
    ))

    apt_settlement = ApartmentSettlement(
        apartment="apart-polanka",
        year=2024,
        month=3,
        total_rent_pln=0.0,
        total_bills_pln=900.0,
        total_due_pln=900.0
    )

    settlements = manager.create_tenant_settlements(apt_settlement)

    assert len(settlements) == 3

    assert all(isinstance(s, TenantSettlement) for s in settlements)

    assert all(s.year == 2024 for s in settlements)

    assert all(s.month == 3 for s in settlements)

    assert all(s.bills_pln == 300.0 for s in settlements)

    assert all(s.total_due_pln == 300.0 for s in settlements)

    tenants = {s.tenant for s in settlements}
    assert tenants == {"Jan Nowak", "Adam Kowalski", "Ewa Adamska"}

    manager.tenants = {
        "t1": manager.tenants["tenant-1"]
    }

    apt_settlement2 = ApartmentSettlement(
        apartment="apart-polanka",
        year=2024,
        month=4,
        total_rent_pln=0.0,
        total_bills_pln=500.0,
        total_due_pln=500.0
    )

    settlements_single = manager.create_tenant_settlements(apt_settlement2)

    assert len(settlements_single) == 1

    assert settlements_single[0].bills_pln == 500.0

    manager.tenants = {}

    apt_settlement3 = ApartmentSettlement(
        apartment="apart-polanka",
        year=2024,
        month=5,
        total_rent_pln=0.0,
        total_bills_pln=700.0,
        total_due_pln=700.0
    )

    settlements_none = manager.create_tenant_settlements(apt_settlement3)

    assert settlements_none == []