from tkinter import *
from tkinter import messagebox
from state import State
from PIL import Image, ImageTk
from load import Load
import api


class Background:
    def __init__(self, img:str):
        self.img = ImageTk.PhotoImage(Image.open(img))

    def draw_canvas(self, root, *args, **kwargs):
        canvas = Canvas(root, bg='white', *args, **kwargs)
        canvas.background = self.img
        canvas.create_image(120, 50, image=self.img, anchor=NW)
        canvas.pack(fill=BOTH, expand=True)
        return canvas

 

class Crew(Frame):
    def __init__(self, *args, app_state:State=None, app_config=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_state = app_state
        self.app_config = app_config
        self.init()
        self.config(highlightthickness=1, highlightbackground='grey')

    def create_releaser_state(self):
        rel = api.get_releaser(self.app_config)
        self.releaser_state = [rel[0]['weight'], 0]

    def switch_releaser_state(self):
        self.releaser_state = self.releaser_state[::-1]

    def create_trooper_sequences(self):
        self.left_trooper_sequence = left_col = api.create_queues()
        self.right_trooper_sequence = right_col = api.create_queues()
        for t in api.get_troopers(self.app_config):
            left_col[0].append(Load(weight=t['weight']/2))
            right_col[0].append(Load(weight=t['weight']/2))

    def update_troopers_btns_state(self, sequence, buttons):
        btns = buttons[::-1]
        col = list(sequence[0])[::-1]

        for idx in range(len(btns)):
            if idx < len(col):
                fg, bg = 'white', 'blue'
                btns[idx].config(fg=fg, bg=bg)
            else:
                fg, bg = 'SystemButtonText', 'SystemButtonFace'
                btns[idx].config(fg=fg, bg=bg)

    def update_rel_btns_state(self):
        btns = self.releaser_btns
        state = self.releaser_state

        for idx in range(len(btns)):
            if state[idx]:
                fg, bg = 'white', 'blue'
                btns[idx].config(fg=fg, bg=bg)
            else:
                fg, bg = 'SystemButtonText', 'SystemButtonFace'
                btns[idx].config(fg=fg, bg=bg)

    def update_rope_btns_state(self, secuence, buttons):
        rope = list(secuence[1])

        for btn in buttons:
            if (len(rope) > 0):
                fg, bg = 'white', 'blue'
                btn.config(fg=fg, bg=bg)
            else:
                fg, bg = 'SystemButtonText', 'SystemButtonFace'
                btn.config(fg=fg, bg=bg)
    
    def update_nav_btns_state(self, sequence, back_btn, fwd_btn):
        col, rope, grd = sequence
        
        if len(rope) == 0 and len(grd) == 0:
            back_btn.config(state='disabled', bg='lightgrey', fg='grey')
            fwd_btn.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')
        elif len(col) == 0 and len(rope) == 0:
            back_btn.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')
            fwd_btn.config(state='disabled', bg='lightgrey', fg='grey')
        else:
            back_btn.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')
            fwd_btn.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')        

    def update_nav_rel_btns_state(self):
        state = self.releaser_state
        if state[0] == 0:
            self.nav_btn_rel_back.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')
            self.nav_btn_rel_forward.config(state='disabled', bg='lightgrey', fg='grey')
        else:
            self.nav_btn_rel_forward.config(state='normal', bg='SystemButtonFace', fg='SystemButtonText')
            self.nav_btn_rel_back.config(state='disabled', bg='lightgrey', fg='grey')

    def show_btn_info(self, btn_type, btn_index):
        weight = 0
        dist = 0
        title = btn_type

        if btn_type == 'releaser':
            title = 'Выпускающий'
            weight = self.releaser_state[btn_index]
            dist = float(self.releaser_btns[btn_index]['text'])
            

        if btn_type == 'left_trooper':
            title = f'Десантник слева: {btn_index+1}'
            buttons = self.left_trooper_btns
            curr_btn = buttons[btn_index]
            reversed_btns = buttons[::-1]
            reversed_seq = list(self.left_trooper_sequence[0])[::-1]
            dist = float(buttons[btn_index]['text'])
            for i in range(len(reversed_btns)):
                if reversed_btns[i] == curr_btn:
                    # print('>>>', i, reversed_seq)
                    if i < len(reversed_seq):
                        weight = reversed_seq[i].weight
                    else:
                        weight = 0

        if btn_type == 'right_trooper':
            title = f'Десантник справа: {btn_index+1}'
            buttons = self.right_troopers_btns
            curr_btn = buttons[btn_index]
            reversed_btns = buttons[::-1]
            reversed_seq = list(self.right_trooper_sequence[0])[::-1]
            dist = float(buttons[btn_index]['text'])
            for i in range(len(reversed_btns)):
                if reversed_btns[i] == curr_btn:
                    # print('>>>', i, reversed_seq)
                    if i < len(reversed_seq):
                        weight = reversed_seq[i].weight
                    else:
                        weight = 0

        if btn_type == 'left_rope':
            title = 'Левый канат'
            dist = float(self.left_rope_btns[0]['text'])
            weight = sum([l.weight for l in list(self.left_trooper_sequence[1])])

        if btn_type == 'right_rope':
            title = 'Правый канат'
            dist = float(self.right_rope_btns[0]['text'])
            weight = sum([l.weight for l in list(self.right_trooper_sequence[1])])

        message = (
                f'- Масса: {weight} кг',
                f'- Плечо: {dist} м',
                f'- Момент: {api.calc_moment(weight=weight, distance=dist)} кгс/м'
            )

        messagebox.Message(title=title, message='\n'.join(message), icon=None).show()

    def calculate_variable_load(self):
        total_weight = 0
        total_moment = 0
        
        total_weight += sum(self.releaser_state)
        rel_dists = [float(b['text']) for b in self.releaser_btns]
        total_moment += sum([api.calc_moment(a, b) for a, b in zip(self.releaser_state, rel_dists)])

        def calc_tr_sequences(btns, sequence):
            nonlocal total_weight, total_moment
            dists = [float(b['text']) for b in btns][::-1]
            weights = [l.weight for l in list(sequence[0])[::-1]]
            zipped_data = [(a,b) for a,b in zip(dists, weights)]
            total_weight += sum([w for d, w in zipped_data])
            total_moment += sum(api.calc_moment(w, d) for d, w in zipped_data)

        calc_tr_sequences(self.left_trooper_btns, self.left_trooper_sequence)
        calc_tr_sequences(self.right_troopers_btns, self.right_trooper_sequence)
        
        rope_weights = [l.weight for l in list(self.left_trooper_sequence[1]) + list(self.right_trooper_sequence[1])]
        rope_dists = [float(self.left_rope_btns[0]['text'])] * len(rope_weights)
        # print('----------')
        # print('>> rope l:', len(rope_weights))
        # print('>> rope w:', rope_weights)
        # print('>> rope d:', rope_dists)
        # print('>> rope m:', [api.calc_moment(a, b) for a, b in zip(rope_weights, rope_dists)])
        total_weight += sum(rope_weights)
        total_moment += sum([api.calc_moment(a, b) for a, b in zip(rope_weights, rope_dists)])
        
        self.app_state.calc_centering(total_weight, total_moment)
            

    def recalculate_variables(self):
        left_rope = self.left_trooper_sequence[1]
        right_rope = self.right_trooper_sequence[1]
        self.rope_count_var.set(value=f'({len(left_rope)}/{len(right_rope)})')
        self.calculate_variable_load()

    def move_left_sec_forward(self):
        api.forward_in_turns(*self.left_trooper_sequence)
        self.update_troopers_btns_state(sequence=self.left_trooper_sequence, buttons=self.left_trooper_btns)
        self.update_rope_btns_state(secuence=self.left_trooper_sequence, buttons=self.left_rope_btns)
        self.recalculate_variables()
        self.update_nav_btns_state(sequence=self.left_trooper_sequence, \
                                   back_btn=self.left_nav_btn_back, fwd_btn=self.left_nav_btn_forward)

    def move_left_sec_back(self):
        api.back_in_turns(*self.left_trooper_sequence)
        self.update_troopers_btns_state(sequence=self.left_trooper_sequence, buttons=self.left_trooper_btns)
        self.update_rope_btns_state(secuence=self.left_trooper_sequence, buttons=self.left_rope_btns)
        self.recalculate_variables()
        self.update_nav_btns_state(sequence=self.left_trooper_sequence, \
                                   back_btn=self.left_nav_btn_back, fwd_btn=self.left_nav_btn_forward)

    def move_right_sec_forward(self):
        api.forward_in_turns(*self.right_trooper_sequence)
        self.update_troopers_btns_state(sequence=self.right_trooper_sequence, buttons=self.right_troopers_btns)
        self.update_rope_btns_state(secuence=self.right_trooper_sequence, buttons=self.right_rope_btns)
        self.recalculate_variables()
        self.update_nav_btns_state(sequence=self.right_trooper_sequence, \
                                   back_btn=self.right_nav_btn_back, fwd_btn=self.right_nav_btn_forward)

    def move_right_sec_back(self):
        api.back_in_turns(*self.right_trooper_sequence)
        self.update_troopers_btns_state(sequence=self.right_trooper_sequence, buttons=self.right_troopers_btns)
        self.update_rope_btns_state(secuence=self.right_trooper_sequence, buttons=self.right_rope_btns)
        self.recalculate_variables()
        self.update_nav_btns_state(sequence=self.right_trooper_sequence, \
                                   back_btn=self.right_nav_btn_back, fwd_btn=self.right_nav_btn_forward) 

    def move_releaser_forward(self):
        # switch rel
        self.switch_releaser_state()
        # update btns state
        self.update_rel_btns_state()
        # recalc vars
        self.recalculate_variables()
        # update nav btns state
        self.update_nav_rel_btns_state()
        pass
    
    def move_releaser_back(self):
        # switch rel
        self.switch_releaser_state()
        # update btns state
        self.update_rel_btns_state()
        # recalc vars
        self.recalculate_variables()
        # update nav btns state
        self.update_nav_rel_btns_state()
        pass

    def init(self):
        bg = Background(img='helicopter5.png')
        canvas = bg.draw_canvas(root=self)
       
        self.start_coords = 40, 180
        self.draw_row_titles(root=canvas)
        self.draw_trooper_btns(root=canvas)
        self.draw_releaser_btns(root=canvas)
        self.draw_rope_btns(root=canvas)
        self.draw_nav_btns(root=canvas)

        self.create_trooper_sequences()
        self.create_releaser_state()
        self.update_troopers_btns_state(sequence=self.left_trooper_sequence, buttons=self.left_trooper_btns)
        self.update_rope_btns_state(secuence=self.left_trooper_sequence, buttons=self.left_rope_btns)
        self.update_troopers_btns_state(sequence=self.right_trooper_sequence, buttons=self.right_troopers_btns)
        self.update_rope_btns_state(secuence=self.right_trooper_sequence, buttons=self.right_rope_btns)
        self.update_nav_btns_state(sequence=self.left_trooper_sequence, \
                                   back_btn=self.left_nav_btn_back, fwd_btn=self.left_nav_btn_forward)
        self.update_nav_btns_state(sequence=self.right_trooper_sequence, \
                                   back_btn=self.right_nav_btn_back, fwd_btn=self.right_nav_btn_forward)
        self.update_nav_rel_btns_state()
        self.update_rel_btns_state()
        self.recalculate_variables()

    def draw_row_titles(self, root):
        rows = self.app_config['rows']
        start_x, start_y = self.start_coords
        self.rope_count_var = StringVar(value='(0/0)')
        start_y += 4
        for i in range(len(rows)):
            row = rows[i];
            Label(root, text=row['type'], bg='white').place(x=start_x, y=start_y + i * 25)
            Label(root, text=i, bg='white').place(x=start_x + 145, y=start_y + i * 25)
            Label(root, text=i, bg='white').place(x=start_x + 380, y=start_y + i * 25)
            # Label(root, text='250 kg', bg='white').place(x=start_x + 400, y=start_y + i * 25)
            if i == len(rows) - 1:
                Label(root, textvariable=self.rope_count_var, bg='white')\
                    .place(x=start_x + 110, y=start_y + i * 25)

    def draw_trooper_btns(self, root):
        start_x, start_y = self.start_coords
        troopers = api.get_troopers(self.app_config)
        troopers_pos = api.get_positions(troopers)
        troopers_dist = api.get_distances(self.app_config, troopers_pos)
        self.left_trooper_btns = left_trooper_btns = []
        self.right_troopers_btns = right_troopers_btns = []
        def create_btn(i):
            dist = troopers_dist[i]
            def l_btn_command():
                self.show_btn_info('left_trooper', i)
            l_btn = Button(root, text=dist, font='Arial 8', width=5, command=l_btn_command)
            l_btn.place(x=start_x + 195, y=start_y + 28 + i * 25)
            left_trooper_btns.append(l_btn)

            def r_btn_command():
                self.show_btn_info('right_trooper', i)
            r_btn = Button(root, text=dist, font='Arial 8', width=5, command=r_btn_command)
            r_btn.place(x=start_x + 300, y=start_y + 28 + i * 25)
            right_troopers_btns.append(r_btn)
        
        for i in range(len(troopers_dist)):
            create_btn(i)
            

    def draw_releaser_btns(self, root):
        start_x, start_y = self.start_coords
        releaser = api.get_releaser(self.app_config)
        releaser_pos = api.get_positions(releaser)
        releaser_dist = api.get_distances(self.app_config, releaser_pos)
        self.releaser_btns = []
        def create_btn(i):
            dist = releaser_dist[i]
            weight = releaser[i]['weight']
            def command():
                self.show_btn_info('releaser', i)
            btn = Button(root, text=dist, font='Arial 8', width=5, command=command)
            btn.place(x=start_x + 248, y=start_y + i * 9.1 * 25)
            self.releaser_btns.append(btn)

        for i in range(len(releaser_dist)):
            create_btn(i)

    def draw_rope_btns(self, root):
        start_x, start_y = self.start_coords       
        rope = api.get_rope(self.app_config)
        rope_pos = api.get_positions(rope)
        rope_dist = api.get_distances(self.app_config, rope_pos)
        self.left_rope_btns = left_rope_btns = []
        self.right_rope_btns = right_rope_btns = []
        def create_btn(i):
            dist = rope_dist[i]
            def l_btn_command():
                self.show_btn_info('left_rope', i)
            l_btn = Button(root, text=dist, font='Arial 8', width=5, command=l_btn_command)
            l_btn.place(x=start_x + 195, y=start_y + 10 * 25)
            left_rope_btns.append(l_btn)
            
            def r_btn_command():
                self.show_btn_info('right_rope', i)
            r_btn = Button(root, text=dist, font='Arial 8', width=5, command=r_btn_command)
            r_btn.place(x=start_x + 300, y=start_y +  10 * 25)
            right_rope_btns.append(r_btn)

        for i in range(len(rope_dist)):
            create_btn(i)

    def draw_nav_btns(self, root):
        start_x, start_y = self.start_coords
        # left trooper sequence
        self.left_nav_btn_back = Button(root, text=u'\u2191', width=4, command=self.move_left_sec_back)
        self.left_nav_btn_back.place(x=start_x + 195, y=start_y - 150)
        self.left_nav_btn_forward = Button(root, text=u'\u2193', width=4, command=self.move_left_sec_forward)
        self.left_nav_btn_forward.place(x=start_x + 195, y=start_y - 120)
        
        # right trooper sequence
        self.right_nav_btn_back = Button(root, text=u'\u2191', width=4, command=self.move_right_sec_back)
        self.right_nav_btn_back.place(x=start_x + 300, y=start_y - 150)
        self.right_nav_btn_forward = Button(root, text=u'\u2193', width=4, command=self.move_right_sec_forward)
        self.right_nav_btn_forward.place(x=start_x + 300, y=start_y - 120)
        
        # releaser moving
        self.nav_btn_rel_back = Button(root, text=u'\u2191', width=4, command=self.move_releaser_back)
        self.nav_btn_rel_back.place(x=start_x + 248, y=start_y - 150)
        self.nav_btn_rel_forward = Button(root, text=u'\u2193', width=4, command=self.move_releaser_forward)
        self.nav_btn_rel_forward.place(x=start_x + 248, y=start_y - 120)
       