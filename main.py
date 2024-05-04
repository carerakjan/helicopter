from tkinter import Tk
from app import App
from api import get_config


def main():
    root = Tk()
    root.geometry('720x640+240+10')
    root.resizable(False, False)
    root.title('Helicopter')
    cfg = get_config()
    app = App(cfg=cfg)
    root.mainloop()

if __name__ == '__main__':
    main()