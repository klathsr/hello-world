from abc import ABC, abstractmethod


class Vehicle(ABC):
    """
    Abstract base class representing a general vehicle.
    """

    def __init__(self, make: str, model: str, year: int):
        if not make or not model or year <= 0:
            raise ValueError("Invalid vehicle information")

        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    @abstractmethod
    def start_engine(self):
        """Start the vehicle engine"""
        pass

    @abstractmethod
    def stop_engine(self):
        """Stop the vehicle engine"""
        pass

    def get_info(self) -> str:
        """Return vehicle basic information"""
        return f"{self.year} {self.make} {self.model}"


class CommercialVehicle:
    """
    Represents a commercial vehicle that can carry cargo.
    """

    def __init__(self, license_number: str, max_load: float):
        if not license_number or max_load <= 0:
            raise ValueError("Invalid commercial vehicle data")

        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0.0

    def load_cargo(self, weight: float) -> bool:
        """Try to load cargo without exceeding max load"""
        if weight <= 0:
            return False

        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            return True
        return False

    def unload_cargo(self, weight: float) -> float:
        """Unload cargo safely"""
        if weight <= 0:
            return self.current_load

        if weight >= self.current_load:
            self.current_load = 0
        else:
            self.current_load -= weight

        return self.current_load


class Car(Vehicle):
    """
    A car that inherits from Vehicle.
    """

    def __init__(self, make: str, model: str, year: int, num_doors: int):
        super().__init__(make, model, year)

        if num_doors <= 0:
            raise ValueError("Number of doors must be positive")

        self.num_doors = num_doors

    def start_engine(self):
        self.is_running = True

    def stop_engine(self):
        self.is_running = False


class Trailer(CommercialVehicle):
    """
    Trailer used for transporting cargo.
    """

    def __init__(self, license_number: str, max_load: float, num_axles: int = 2):
        super().__init__(license_number, max_load)

        if num_axles <= 0:
            raise ValueError("Number of axles must be positive")

        self.num_axles = num_axles

    def get_weight_per_axle(self) -> float:
        """Return weight distributed per axle"""
        if self.num_axles == 0:
            return 0
        return self.current_load / self.num_axles


class DeliveryVan(Car, CommercialVehicle):
    """
    Delivery van using multiple inheritance.
    """

    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        num_doors: int,
        license_number: str,
        max_load: float,
    ):
        Car.__init__(self, make, model, year, num_doors)
        CommercialVehicle.__init__(self, license_number, max_load)

        self.delivery_mode = False

    def toggle_delivery_mode(self) -> str:
        """Toggle delivery mode on or off"""
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode {'ON' if self.delivery_mode else 'OFF'}"

    def get_info(self) -> str:
        """Override to include commercial info"""
        return (
            f"{super().get_info()}, "
            f"License: {self.license_number}, "
            f"Load: {self.current_load}/{self.max_load}"
        )

    def begin_service(self):
        """Simulate a delivery service process"""
        print(self.get_info())

        self.load_cargo(50)
        self.start_engine()
        print(self.toggle_delivery_mode())

        self.stop_engine()
        self.unload_cargo(50)
        print(self.toggle_delivery_mode())


# =======================
# Test Section
# =======================
if __name__ == "__main__":
    van = DeliveryVan(
        make="Toyota",
        model="HiAce",
        year=2023,
        num_doors=4,
        license_number="AB-1234",
        max_load=500,
    )

    van.begin_service()