from src.models import Apartment, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()
        
    def __init__(self):
        self.apartments = {}
        
    def add_apartment(self, key, apartment):
        self.apartments[key] = apartment
        
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