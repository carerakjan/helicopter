from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Load:
    weight: float = 0
    moment: float = 0
    distance: float = 0

    def calc_moment(self):
        self.moment = round(self.weight * self.distance, 3)
    
    def calc_distance(self):
        self.distance = round(self.moment / self.weight, 3)

    def calc_weight(self):
        self.weight = round(self.moment / self.distance, 3)