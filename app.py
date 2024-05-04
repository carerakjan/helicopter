from tkinter import *
from state import StateSimple
from settings import Settings
from crew import Crew
import api

class App(Frame):
    def __init__(self, *args, cfg = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_state = StateSimple(cfg=cfg)
        self.app_config = cfg
        self.init_ui()
    
    def init_ui(self):
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, pad=7)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        labels_container = Frame(self)
        labels_container.grid(sticky=W, column=2, row=0)

        lbl_frame_common = LabelFrame(labels_container, border=1, text=' Вертольот ')
        lbl_frame_common.pack(anchor=W, fill=BOTH, padx=5, pady=5)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text=' Пустая масса (кг):').pack(side=LEFT)
        Label(lbl_frame, text=api.get_empty_helicopter_load(self.app_config).weight).pack(side=RIGHT)  
        
        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text=' Постоянная загрузка (кг):').pack(side=LEFT)
        Label(lbl_frame, text=api.get_constant_load(self.app_config).weight).pack(side=RIGHT)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text=' Общая масса (кг):').pack(side=LEFT)
        Label(lbl_frame, textvariable=self.app_state.total_load_var).pack(side=RIGHT)
        
        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text=' Изменяемая загрузка (кг):').pack(side=LEFT)
        Label(lbl_frame, textvariable=self.app_state.variable_load_var).pack(side=RIGHT)

        # -------------------------
        lbl_frame_common = LabelFrame(labels_container, border=1)
        lbl_frame_common.pack(anchor=W, fill=BOTH, padx=5, pady=15)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text='Граничная перед.\nцентровка (м): ', justify=LEFT).pack(side=LEFT)
        Label(lbl_frame, text=api.get_centering_limits(self.app_config)[0]).pack(side=RIGHT)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text='Граничная задняя\nцентровка (м): ', justify=LEFT).pack(side=LEFT)
        Label(lbl_frame, text=api.get_centering_limits(self.app_config)[1]).pack(side=RIGHT)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text='Центровка (м): ').pack(side=LEFT)
        Label(lbl_frame, textvariable=self.app_state.centering_var).pack(side=RIGHT)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text='Превышение перед.\nцентровки (м): ', justify=LEFT).pack(side=LEFT)
        Label(lbl_frame, textvariable=self.app_state.front_limit_exceeding_var).pack(side=RIGHT)

        lbl_frame = LabelFrame(lbl_frame_common, border='0')
        lbl_frame.pack(anchor=W, fill=BOTH, padx=7, pady=2)
        Label(lbl_frame, text='Превышение задней\nцентровки (м): ', justify=LEFT).pack(side=LEFT)
        Label(lbl_frame, textvariable=self.app_state.rare_limit_exceeding_var).pack(side=RIGHT)
        # -------------------------

        area = Crew(self, app_state=self.app_state, app_config=self.app_config)
        area.grid(row=0, column=0, columnspan=2, rowspan=4, padx=5, pady=5, sticky=E+W+S+N)

        # settings = Settings(self, app_state=self.app_state, app_config=self.app_config)
        # settings.grid(sticky=W, padx=5, pady=4, column=3, row=1)