from psychopy import visual, event, core
import numpy as np
import json


def generate_references(dim=[4,3]):
    row, col = dim;
    n_tiles = row*col;
    if n_tiles > 35:
        return "Too much tiles add more images and remove this trigger"
    img = [f"{i}.png" for i in range(1, n_tiles+1)];
    player = [f"{i}" for i in range(n_tiles)];
    
    ref = dict(zip(player, img))

    return ref


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
    
# Create a class to group stimuli
class StimGroup:
    def __init__(self, win, stimuli):
        self.win = win
        self.stimuli = stimuli

    def draw(self):
        for stim in self.stimuli:
            stim.draw()


def mini_map(win,pos,map,dim=[4,3],col = "#719b00",offset = [0.42,0.31]):
    '''Create a minimap object that you will be able to draw later'''
    offset_x,offset_y = offset;
    offset_x = offset_x*win.size[0];
    offset_y = offset_y*win.size[1];
    map_height = win.size[1]/4;
    n_tiles = dim[0]*dim[1];

    if map == 'circle':
        st_off = 9; #Change that if you want the starting point of the cirle to be somewhere else
        r = 0.4*map_height; #Radius
        theta = (n_tiles-(pos+st_off)%n_tiles) * (2*np.pi/n_tiles); #theta angle
        x = np.cos(theta)*r  # X-coordinate
        y = np.sin(theta)*r  # Y-coordinate
        dot = visual.Circle(win, radius=0.2*r, pos=(x+offset_x*1.02, y+offset_y*1.2), fillColor=col);
        frame = visual.Rect(win, width=2.5*r,height=2.5*r,pos=(offset_x*1.02, offset_y*1.2),lineWidth = 0.5*r,lineColor ='#674928');
        map_obj = StimGroup(win,[dot,frame]);
        return map_obj
    elif map =='taurus':
        space_x = np.linspace(-1,1,dim[1]);
        space_y = np.linspace(-1,1,dim[0]);
        
        pos_x = space_x[pos%dim[1]];
        pos_y = space_y[pos//dim[1]];
        
        dot = visual.Circle(win,radius= 0.08*map_height,color=col,pos=(offset_x + ((map_height*dim[1])/(2*dim[0]))*pos_x,offset_y + (map_height/2)*pos_y));
        frame = visual.Rect(win, width=map_height*1.5*(dim[1]/dim[0]),height=map_height*1.5,pos=(offset_x, offset_y),lineWidth = 0.05*map_height,lineColor ='#674928');
        map_obj = StimGroup(win,[dot,frame]);
        #Groupe with rect
        return map_obj 
    else:
        return "unknown map"

