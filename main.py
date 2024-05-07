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
    def draw_table(self, data):
        self.table = Table(self)
        self.table.draw_json(data)
        self.mainloop()

class AppMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_items()

    def add_items(self):
        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label='Параметры вертольота')
        editmenu.add_command(label='Постоянная загрузка', command=self.show_edit_dialog)
        self.add_cascade(label='Редактировать', menu=editmenu)

    def show_edit_dialog(self):
        if self.table_data:
            EditWindow(self).draw_table(self.table_data)
        
    def set_table_data(self, data):
        self.table_data = data

def main():
    root = Tk()
    mainmenu = AppMenu(root)
    root.geometry('720x640+240+10')
    root.resizable(False, False)
    root.title('Helicopter')
    root.config(menu=mainmenu)

    cfg = get_config()
    app = App(cfg=cfg)
    mainmenu.set_table_data(cfg['load'])
    root.mainloop()

if __name__ == '__main__':
    main()