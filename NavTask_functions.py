from psychopy import visual, event, core


def new_position(pos,action,map,dim=[4,3]):
    '''Compute the new position in a taurus or a circle the position are in N and [0:n_tiles]
        dim = [row,col]'''
    row, col = dim;
    n_tiles = row*col;
    if map == 'circle':
        if action == 'right':
            new_pos = (pos + 1)%n_tiles;
        elif action == 'left':
            new_pos = (pos - 1)%n_tiles;
        elif action == 'up':
            new_pos = (pos + 2)%n_tiles;
        elif action == 'down':
            new_pos = (pos - 2)%n_tiles;
    elif map == 'taurus':
        if action == 'right':
            new_pos = (pos//col)*col+(pos+1)%col;
        elif action == 'left':
            new_pos = (pos//col)*col+(pos-1)%col;
        elif action == 'up':
            new_pos = (pos+col)%n_tiles;
        elif action == 'down':
            new_pos = (pos-col)%n_tiles;
    else:
        return "unknown map"
    return new_pos

win = visual.Window(units='pix', fullscr=True, color='black');


pos=1;
dim = [4,3]
MAP = ['taurus','circle'];
map_index = 0;
map = MAP[map_index];
print(map);

text = visual.TextStim(win, text=pos,color="white", height=.08*win.size[1],pos=(0,0));
text.draw();
win.flip();

while True:
    print(pos);
    keys = event.waitKeys();
    if 'escape' in keys:
        break
    elif 'z' in keys:
        pos = new_position(pos,'up',map,dim=dim);
    elif 's' in keys:
        pos = new_position(pos,'down',map,dim=dim);
    elif 'q' in keys:
        pos = new_position(pos,'left',map,dim=dim);
    elif 'd' in keys:
        pos = new_position(pos,'right',map,dim=dim);
    elif 'm' in keys:
        map_index+=1;
        map_index = map_index%2;
        map = MAP[map_index];
        print(map);
        text_map = visual.TextStim(win, text=f"Map change to {map}",color="white", height=.08*win.size[1],pos=(0,-0.2*win.size[1]));
        text_map.draw();
        
    text = visual.TextStim(win, text=pos,color="white", height=.08*win.size[1],pos=(0,0));
    text.draw();
    win.flip();

win.close();
core.quit();