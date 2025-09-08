class VehicleAd:
    def __init__(self, title, publication_date, link, price, currency, make=None, model=None, year=None, mileage=None, fuel_type=None,
                 gearbox=None, vehicle_type=None, engine_capacity=None):
        self.title = title
        self.publication_date = publication_date
        self.link = link
        self.price = price
        self.currency = currency

        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.fuel_type = fuel_type
        self.gearbox = gearbox
        self.vehicle_type = vehicle_type
        self.engine_capacity = engine_capacity

    def to_json(self):
        return {
            "title": self.title,
            "publication_date": self.publication_date,
            "link": self.link,
            "price": self.price,
            "currency": self.currency,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "fuel_type": self.fuel_type,
            "gearbox": self.gearbox,
            "vehicle_type": self.vehicle_type,
            "engine_capacity": self.engine_capacity
        }
    def __str__(self):
        return f"{self.link} \n {self.title} - {self.publication_date} - {self.price} {self.currency} - {self.year} - {self.mileage} - {self.fuel_type} - {self.gearbox} - {self.vehicle_type} - {self.engine_capacity}"

    def __repr__(self):
        return self.__str__()