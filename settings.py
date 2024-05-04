from tkinter import *
from state import State
from config import Config

class Settings(Frame):
    def __init__(self, *args, app_state:State=None, app_config:Config = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_state = app_state
        self.app_config = app_config
        self.init()

    def init(self):
        lbl_bordered = LabelFrame(self, text=' Settings ', borderwidth=1, padx=10, pady=10)
        lbl_bordered.pack(fill=BOTH)

        lbl_id = Label(lbl_bordered, font='Helvetica 12 bold', textvariable=self.app_state.text)
        lbl_id.pack(anchor=W)

        chb_enable = Checkbutton(lbl_bordered, text='On/off', variable=self.app_state.enabled)
        chb_enable.pack(anchor=W, pady=4)

        lbl_weight = Label(lbl_bordered, text='Weight (kg):')
        lbl_weight.pack(anchor=W)

        txt_weight = Entry(lbl_bordered, textvariable=self.app_state.weight)
        txt_weight.pack(anchor=W)

        lbl_weight = Label(lbl_bordered, text='Distance (m):')
        lbl_weight.pack(anchor=W, pady=(10,0))

        txt_weight = Entry(lbl_bordered, textvariable=self.app_state.distance)
        txt_weight.pack(anchor=W)

        lbl_weight = Label(lbl_bordered, text='Moment (kgf/m2):')
        lbl_weight.pack(anchor=W, pady=(10,0))

        txt_weight = Entry(lbl_bordered, textvariable=self.app_state.moment, state='readonly')
        txt_weight.pack(anchor=W)

        clc_bordered = LabelFrame(self, text=' Helicopter ', borderwidth=1, padx=10, pady=10)
        clc_bordered.pack(pady=(10,0), fill=BOTH)
        Label(clc_bordered, text=f'Weight (kg): {self.app_config.empty_helicopter.weight}').pack(anchor=W)
        Label(clc_bordered, text=f'Moment (kgf/m2): {self.app_config.empty_helicopter.moment}').pack(anchor=W)

        clc_bordered = LabelFrame(self, text=' Constant Load ', borderwidth=1, padx=10, pady=10)
        clc_bordered.pack(pady=(10,0), fill=BOTH)
        Label(clc_bordered, text=f'Weight (kg): {self.app_config.constant_load.weight}').pack(anchor=W)
        Label(clc_bordered, text=f'Moment (kgf/m2): {self.app_config.constant_load.moment}').pack(anchor=W)

        clc_bordered = LabelFrame(self, text=' Load of troopers ', borderwidth=1, padx=10, pady=10, height=80)
        clc_bordered.pack(pady=(10,0), fill=BOTH)
        Label(clc_bordered, text='Weight (kg):').place(x=0, y=0)
        Label(clc_bordered, textvariable=self.app_state.total_weight).place(x=70, y=0)
        Label(clc_bordered, text='Moment:').place(x=0, y=20)
        Label(clc_bordered, textvariable=self.app_state.total_moment).place(x=70, y=20)

        Label(self, text='Центровка (м):').pack(anchor=W)

        centering_var = StringVar()

        def update_centering_value(*args):
            total_moments = float(self.app_config.empty_helicopter.moment) + float(self.app_config.constant_load.moment) + float(self.app_state.total_moment.get())
            total_weights = float(self.app_config.empty_helicopter.weight) + float(self.app_config.constant_load.weight) + float(self.app_state.total_weight.get())
            centering_var.set(value=total_moments/total_weights)

        self.app_state.total_moment.trace_add(mode='write', callback=update_centering_value)
        self.app_state.total_weight.trace_add(mode='write', callback=update_centering_value)
        update_centering_value()
        Label(self, textvariable=centering_var).pack(anchor=W)

        front_limit_exceeding = StringVar(value='-')
        rare_limit_exceeding = StringVar(value='-')

        def calc_exceeding(*args):
            centering_num = float(centering_var.get())
            print(centering_num , self.app_config.front_limit_centering, centering_num > self.app_config.front_limit_centering)
            
            front_limit_exceeding.set(value='-')
            rare_limit_exceeding.set(value='-')
            
            if centering_num > self.app_config.front_limit_centering:
                front_limit_exceeding.set(value=centering_num - self.app_config.front_limit_centering)

            if centering_num < self.app_config.rear_limit_centering:
                rare_limit_exceeding.set(value=abs(centering_num - self.app_config.rear_limit_centering))

        calc_exceeding()

        centering_var.trace_add(mode='write', callback=calc_exceeding)

        Label(self, text='Превышение передней центровки на (м):').pack(anchor=W)
        Label(self, textvariable=front_limit_exceeding).pack(anchor=W)

        Label(self, text='Превышение задней центровки на (м):').pack(anchor=W)
        Label(self, textvariable=rare_limit_exceeding).pack(anchor=W)