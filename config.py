import json
from dataclasses import dataclass

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



@dataclass
class Trooper(Load):
    row: int = -1
    type: str = 'Д'
    enabled: bool = True


class Config:
    def load(self):
        with open('config.json', encoding='utf-8') as file:
            cfg = json.load(file)

            helicopter = cfg['helicopter']
            self.empty_helicopter = Load(weight=helicopter['weight'], moment=helicopter['moment'], distance=helicopter['distance'])
            
            load_list = cfg['load']
            load_total_weight = 0
            load_total_moment = 0

            for it in load_list:
                load_total_weight += it['weight']
                load_total_moment += it['moment']
            
            self.constant_load = Load(weight=load_total_weight, moment=round(load_total_moment, 3))
            
            self.releaser = []
            self.troopers = []
            self.rope = []
            self.rows = cfg['rows']
            self.front_limit_centering = cfg['frontLimit']
            self.rear_limit_centering = cfg['rearLimit']

            for item in cfg['rope']:
                self.rope.append(Trooper(
                    weight= item['weight'],
                    moment=item['moment'],
                    distance=item['distance'],
                    row=item['row'],
                    type='К',
                    enabled=item['enabled']
                ))

            for item in cfg['releaser']:
                self.releaser.append(Trooper(
                    weight= item['weight'],
                    moment=item['moment'],
                    distance=item['distance'],
                    row=item['row'],
                    type='В',
                    enabled=item['enabled']
                ))

            for item in cfg['paratroopers']:
                self.troopers.append(Trooper(
                    weight= item['weight'],
                    moment=item['moment'],
                    distance=item['distance'],
                    row=item['row'],
                    enabled=item['enabled']
                ))

        return self