import json
from load import Load
from collections import deque

CONFIG_FILE = 'config.json'

def get_config():
    with open(CONFIG_FILE, encoding='utf-8') as file:
        return json.load(file)


def get_constant_load(cfg):
    load_list = cfg['load']
    load_total_weight = 0
    load_total_moment = 0

    for it in load_list:
        load_total_weight += it['weight']
        load_total_moment += it['moment']
    
    return Load(weight=round(load_total_weight, 3), moment=round(load_total_moment, 3))


def get_empty_helicopter_load(cfg):
    helicopter = cfg['helicopter']
    return Load(weight=helicopter['weight'], distance=helicopter['distance'])

def get_centering_limits(cfg):
    front_limit = cfg['frontLimit']
    rear_limit = cfg['rearLimit']
    return front_limit, rear_limit


def create_queues():
    column = deque(maxlen=8)
    rope = deque(maxlen=3)
    ground = deque(maxlen=8)
    return column, rope, ground


def back_in_turns(column, rope, ground):
    if len(ground) > 0:
        fst = rope[0] if len(rope) > 0 else None
        rope.append(ground.popleft())

        if fst is not None and fst not in rope:
            column.append(fst)
    elif len(rope) > 0:
        column.append(rope.popleft())


def forward_in_turns(column, rope, ground):
    if len(column) > 0:
        lst = rope[-1] if len(rope) > 0 else None
        rope.appendleft(column.pop())

        if lst is not None and lst not in rope:
            ground.appendleft(lst)
    elif len(rope) > 0:
        ground.appendleft(rope.pop())


def get_troopers(cfg):
    return [t for t in cfg['paratroopers'] if 'type' not in t]


def get_releaser(cfg):
    return [t for t in cfg['paratroopers'] if 'type' in t and t['type'] == 'releaser']


def get_rope(cfg):
    return [t for t in cfg['paratroopers'] if 'type' in t and t['type'] == 'rope']


def get_positions(troopers):
    return [p['row'] for p in troopers]


def get_distances(cfg, positions):
    return [r['distance'] for r in cfg['rows'] if r['id'] in positions]


def calc_moment(weight, distance):
    l = Load(weight=weight, distance=distance)
    l.calc_moment()
    return l.moment



# dev
if __name__ == '__main__':
    cfg = get_config()
    troopers = get_troopers(cfg)
    troopers_pos = get_positions(troopers)
    troopers_dist = get_distances(cfg, troopers_pos)
    # print(troopers)
    
    rel = get_releaser(cfg)
    rel_pos = get_positions(rel)
    rel_dist = get_distances(cfg, rel_pos)
    r1 = [rel[0]['weight'], 0]

    print('wei: ', r1)
    print('pos: ', rel_pos)
    print('dis: ', rel_dist)
    print('mom: ', [calc_moment(r1[i], rel_dist[i]) for i in range(len(r1))])

    r1 = r1[::-1]

    print('wei: ', r1)
    print('pos: ', rel_pos)
    print('dis: ', rel_dist)
    print('mom: ', [calc_moment(r1[i], rel_dist[i]) for i in range(len(r1))])


    rope = get_rope(cfg)
    rope_pos = get_positions(rope)
    # print(rope)

    # col, rp, grd = create_queues()

    # for it in troopers:
    #     col.append(it['weight'])

    # def pretty_print(lst):
    #     if len(lst) > 0:
    #         print('[', end='')
    #     else:
    #         print(lst)
    #     for i in range(len(lst)):
    #         it = lst[i]
    #         print(f'{it:^8}', end=' | ' if i < len(lst)-1 else ']\n')

    # pretty_print(list(col)[::-1])
    # pretty_print(troopers_dist[::-1])
    # pretty_print([calc_moment(list(col)[::-1][i], troopers_dist[::-1][i]) for i in range(len(list(col)))])

    # print('---- moving start: ---')
    # for i in range(10):
    #     print(f'<<<<<-----{i+1}')
    #     forward_in_turns(col, rp, grd)
    #     pretty_print(list(col)[::-1])
    #     pretty_print(troopers_dist[::-1])
    #     pretty_print([calc_moment(list(col)[::-1][i], troopers_dist[::-1][i]) for i in range(len(list(col)))])

    # print('\n\n\n---start moving back: ---')

    # for i in range(17):
    #     print(f'{i+1}---->>>>>>')
    #     back_in_turns(col, rp, grd)
    #     pretty_print(list(col)[::-1])
    #     pretty_print(troopers_dist[::-1])
    #     pretty_print([calc_moment(list(col)[::-1][i], troopers_dist[::-1][i]) for i in range(len(list(col)))])

