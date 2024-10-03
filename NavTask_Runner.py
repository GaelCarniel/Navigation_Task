from psychopy import visual, event, core

from NavTask_functions import *


win = visual.Window(units='pix', fullscr=True, color='black');


pos=1;#Initialise the position 
dim = [4,3]; #Maps dimension 
ref_table = generate_references(dim);
print(ref_table);
MAP = ['taurus','circle'];
map_index = 0;
map = MAP[map_index];


text_map = visual.TextStim(win, text=f"Map is {map}",color="white", height=.08*win.size[1],pos=(0,-0.2*win.size[1]),wrapWidth = 0.8*win.size[0]);
text_map.draw();
text = visual.TextStim(win, text=pos,color="white", height=.08*win.size[1],pos=(0,0.3*win.size[1]));
text.draw();
room = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(pos)]}", size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,-0.1)); 
room.draw()

dot = mini_map(win,pos,map);
dot.draw();
win.flip();

while True:
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
        text_map = visual.TextStim(win, text=f"Map change to {map}",color="white", height=.08*win.size[1],pos=(0,-0.2*win.size[1]),wrapWidth = 0.8*win.size[0]);
        text_map.draw();
        
    text = visual.TextStim(win, text=pos,color="white", height=.08*win.size[1],pos=(0,0.3*win.size[1]));
    text.draw();
    room = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(pos)]}", size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,-0.1)); 
    room.draw()
    dot = mini_map(win,pos,map);
    dot.draw();
    win.flip();

win.close();
core.quit();