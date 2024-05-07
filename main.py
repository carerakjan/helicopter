from tkinter import Tk, Menu, Frame, Text, INSERT, Toplevel
from app import App
from api import get_config

class Table(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare_json_data(self, data):
        columns = tuple(data[0].keys())
        return columns, [tuple(it.values()) for it in data]

    def draw_json(self, data):
        cols, rows = self.prepare_json_data(data)
   
        for j, col in enumerate(cols):
            text = Text(self, width=30, height=1, bg="#9bc2e6")
            text.grid(row=0, column=j, padx=1, pady=1)
            text.insert(INSERT, col)
            text.config(state='disabled')

        for i in range(len(rows)):
            for j in range(len(cols)):
                text = Text(self, width=30, height=1)
                text.grid(row=i+1, column=j, padx=1, pady=1)
                text.insert(INSERT, rows[i][j])

        self.pack()

class EditWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol('WM_DELETE_WINDOW', self.on_destroy_window)
    
    def on_destroy_window(self):
        self.master.is_edit_dialog_opened = False
        self.destroy()  

    def draw_table(self, data):
        self.table = Table(self)
        self.table.draw_json(data)
        self.mainloop()

class AppMenu(Menu):
    def __init__(self, *args, cfg = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_config = cfg
        self.add_items()
        self.is_edit_dialog_opened  = False

    def add_items(self):
        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label='Параметры вертольота', command=self.show_edit_helicopter_settings)
        editmenu.add_command(label='Постоянная загрузка', command=self.show_edit_constant_load)
        self.add_cascade(label='Редактировать', menu=editmenu)

    def show_edit_constant_load(self):
        if self.app_config and not self.is_edit_dialog_opened:
            self.is_edit_dialog_opened = True
            EditWindow(self).draw_table(self.app_config['load'])

    def show_edit_helicopter_settings(self):
        if self.app_config and not self.is_edit_dialog_opened:
            self.is_edit_dialog_opened = True
            EditWindow(self)
    

def main():
    root = Tk()
    cfg = get_config()
    mainmenu = AppMenu(root, cfg=cfg)
    root.geometry('720x640+240+10')
    root.resizable(False, False)
    root.title('Helicopter')
    root.config(menu=mainmenu)

    app = App(cfg=cfg)
    root.mainloop()

if __name__ == '__main__':
    main()