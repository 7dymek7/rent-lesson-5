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
        apartment = self.apartments.get(apartment_key)
        if apartment is None:
            return None
        
        if month is not None and not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month}")
        
        bills = apartment.bills
        
        if year is not None:
            bills = [b for b in bills if b.year == year]
            
        if month is not None:
            bills = [b for b in bills if b.month == month]
            
        return sum(b.amount for b in bills) if bills else 0.0
    
    
    


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