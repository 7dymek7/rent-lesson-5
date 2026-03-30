from src.models import (
    Apartment,
    Bill,
    Parameters,
    Tenant,
    Transfer,
    ApartmentSettlement,
    TenantSettlement,
)


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

        self.apartments: dict[str, Apartment] = {}
        self.tenants: dict[str, Tenant] = {}
        self.transfers: list[Transfer] = []
        self.bills: list[Bill] = []

        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(self, apartment_key, year=None, month=None):
        apartment_bills = [b for b in self.bills if b.apartment == apartment_key]

        if not apartment_bills:
            return None

        if month is not None and not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month}")

        filtered = apartment_bills

        if year is not None:
            filtered = [b for b in filtered if b.settlement_year == year]

        if month is not None:
            filtered = [b for b in filtered if b.settlement_month == month]

        if not filtered:
            return 0.0

        return sum(b.amount_pln for b in filtered)

    def create_apartment_settlement(self, apartment_key: str, year: int, month: int):
        bills = [
            b for b in self.bills
            if b.apartment == apartment_key
            and b.settlement_year == year
            and b.settlement_month == month
        ]

        total_bills = sum(b.amount_pln for b in bills)
        total_rent = 0.0
        total_due = total_bills - total_rent

        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_rent_pln=total_rent,
            total_bills_pln=total_bills,
            total_due_pln=total_due,
        )

    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement):
        tenants = [
            t for t in self.tenants.values()
            if t.apartment == apartment_settlement.apartment
        ]

        if not tenants:
            return []

        cost_per_tenant = apartment_settlement.total_bills_pln / len(tenants)

        settlements: list[TenantSettlement] = []

        for tenant in tenants:
            settlements.append(TenantSettlement(
                tenant=tenant.name,
                apartment_settlement=apartment_settlement.apartment,
                year=apartment_settlement.year,
                month=apartment_settlement.month,
                rent_pln=0.0,
                bills_pln=cost_per_tenant,
                total_due_pln=cost_per_tenant,
                balance_pln=0.0,
            ))

        return settlements
