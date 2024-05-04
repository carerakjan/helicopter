from tkinter import BooleanVar, StringVar
from dataclasses import dataclass
import api

@dataclass
class AbstractItem:
    weight: StringVar
    enabled: BooleanVar
    type: StringVar
    text: StringVar
    distance: StringVar
    moment: StringVar

    def values()-> tuple[bool, str, str, str, str, str]:
        pass

    def calc_moment():
        pass


class Item(AbstractItem):
    def __init__(self, weight: str, enabled: bool, type: str, distance: str, moment: str) -> None:
        self.id = id(self)
        self.is_active = BooleanVar(value=False)
        AbstractItem.__init__(self, weight=StringVar(value=weight), enabled=BooleanVar(value=enabled), 
                              type=StringVar(value=type), text=StringVar(value=type), 
                              distance=StringVar(value=distance), moment=StringVar(value=moment))

    def values(self):
        return self.enabled.get(), self.weight.get(), self.text.get(), self.type.get(), self.distance.get(), self.moment.get()

    def calc_moment(self):
        try:
            weight = self.weight.get()
            distance = self.distance.get()
            self.moment.set(round(float(weight) * float(distance), 3))
        except Exception:
            pass

        

class State(AbstractItem):
    items = []

    def __init__(self):
        AbstractItem.__init__(self, weight=StringVar(value=''), enabled=BooleanVar(value=False), 
                              type=StringVar(value=''), text=StringVar(value=''), 
                              distance=StringVar(value=''), moment=StringVar(value=''))
        self._active = None
        self.total_weight = StringVar(value='')
        self.total_moment = StringVar(value='')
        self.trace_active()

    def calc_totals(self):
        self.total_weight.set(sum([float(i.weight.get()) for i in self.items if i.enabled.get()]))
        self.total_moment.set(sum([float(i.moment.get()) for i in self.items if i.enabled.get()]))

    def add_item(self, item:Item):
        self.items.append(item)
        self.calc_totals()
    
    def set_active(self, item:Item):
        enabled, weight, text, type, distance, moment = item.values()
        if self._active:
            self._active.is_active.set(False)

        self._active = item
        self._active.is_active.set(True)
        
        self.type.set(type)
        self.text.set(text)
        self.weight.set(weight)
        self.enabled.set(enabled)
        self.distance.set(distance)
        self.moment.set(moment)

    def trace_active(self):
        def update_enabled(*_):
            if self._active is not None:
                self._active.enabled.set(self.enabled.get())
                self.calc_totals()

        def update_weight(*_):
            if self._active is not None:
                self._active.weight.set(self.weight.get())
                self._active.calc_moment()
                self.moment.set(self._active.moment.get())
                self.calc_totals()

        def update_distance(*_):
            if self._active is not None:
                self._active.distance.set(self.distance.get())
                self._active.calc_moment()
                self.moment.set(self._active.moment.get())
                self.calc_totals()

        self.enabled.trace_add('write', update_enabled)
        self.weight.trace_add('write', update_weight)
        self.distance.trace_add('write', update_distance)


class StateSimple:
    def __init__(self, cfg) -> None:
        self.config = cfg
        self.centering_var = StringVar(value='')
        self.variable_load_var = StringVar(value='')
        self.total_load_var = StringVar(value='')
        self.front_limit_exceeding_var = StringVar(value='')
        self.rare_limit_exceeding_var = StringVar(value='')
        self.precision = 3
    
    def calc_centering(self, total_variable_weight, total_variable_moment):
        helicopter = api.get_empty_helicopter_load(self.config)
        constant_load = api.get_constant_load(self.config)
        front_limit, rear_limit = api.get_centering_limits(self.config)

        total_weight = total_variable_weight + helicopter.weight + constant_load.weight
        total_moment = total_variable_moment + helicopter.moment + constant_load.moment
        
        self.variable_load_var.set(value=round(total_variable_weight, self.precision))
        self.total_load_var.set(value=round(total_weight, self.precision))

        centering_num = round(total_moment / total_weight, self.precision)
        self.centering_var.set(value=centering_num)
        
        if centering_num > front_limit:
            self.front_limit_exceeding_var.set(value=round(centering_num - front_limit, self.precision))

        if centering_num < rear_limit:    
            self.rare_limit_exceeding_var.set(value=abs(round(centering_num - rear_limit, self.precision)))
