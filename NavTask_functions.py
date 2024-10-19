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
    
    ref = dict(zip(player, img));

    # Open the JSON file and load the data
    with open("Input/reference_symbol.json", 'r') as file:
        sym = json.load(file);
    
    
    colors = np.random.choice(['blue','red'],2,replace=False);
    col = {'taurus':colors[0],'circle':colors[1]};
    
    reference = {'position':ref,'symbol':sym,'color':col};
    print(reference);
    
    return reference


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
        self.win = win;
        self.stimuli = stimuli;

    def draw(self):
        for stim in self.stimuli:
            print(stim);
            stim.draw();


def mini_map(win,pos,map,global_dict,dim=[4,3],col = "#719b00",offset = [0.42,0.31]):
    '''Create a minimap object that you will be able to draw later'''
    offset_x,offset_y = offset;
    offset_x = offset_x*win.size[0];
    offset_y = offset_y*win.size[1];
    map_height = win.size[1]/4;
    n_tiles = dim[0]*dim[1];
    cols = global_dict['color'];
    if map == 'circle':
        bg_dots=[];
        st_off = 9; #Change that if you want the starting point of the cirle to be somewhere else
        r = 0.4*map_height; #Radius
        for i in range(n_tiles):
            if i!=pos:
                theta = (n_tiles-(i+st_off)%n_tiles) * (2*np.pi/n_tiles); #theta angle
                x = np.cos(theta)*r  # X-coordinate
                y = np.sin(theta)*r  # Y-coordinate
                dot = visual.Circle(win, radius=0.5*0.2*r, pos=(x+offset_x*1.02, y+offset_y*1.2), fillColor='#888888');
                bg_dots.append(dot);

        theta = (n_tiles-(pos+st_off)%n_tiles) * (2*np.pi/n_tiles); #theta angle
        x = np.cos(theta)*r  # X-coordinate
        y = np.sin(theta)*r  # Y-coordinate
        dot = visual.Circle(win, radius=0.2*r, pos=(x+offset_x*1.02, y+offset_y*1.2), fillColor=col);
        frame = visual.Rect(win, width=2.5*r,height=2.5*r,pos=(offset_x*1.02, offset_y*1.2),lineWidth = 0.5*r,lineColor =cols['circle']);
        bg_dots.append(frame);
        bg_dots.append(dot);
        map_obj = StimGroup(win,bg_dots);
        return map_obj
    elif map =='taurus':
        space_x = np.linspace(-1,1,dim[1]);
        space_y = np.linspace(-1,1,dim[0]);
        bg_dots = [];
        for i in range(n_tiles):
            if i!=pos:
                pos_x = space_x[i%dim[1]];
                pos_y = space_y[i//dim[1]];
                dot = visual.Circle(win,radius= 0.5*0.08*map_height,color='#888888',pos=(offset_x + ((map_height*dim[1])/(2*dim[0]))*pos_x,offset_y + (map_height/2)*pos_y));
                bg_dots.append(dot);

        
        pos_x = space_x[pos%dim[1]];
        pos_y = space_y[pos//dim[1]];
        
        dot = visual.Circle(win,radius= 0.08*map_height,color=col,pos=(offset_x + ((map_height*dim[1])/(2*dim[0]))*pos_x,offset_y + (map_height/2)*pos_y));
        frame = visual.Rect(win, width=map_height*1.5*(dim[1]/dim[0]),height=map_height*1.5,pos=(offset_x, offset_y),lineWidth = 0.05*map_height,lineColor =cols['taurus']);
        bg_dots.append(frame);
        bg_dots.append(dot);
        map_obj = StimGroup(win,bg_dots);
        #Groupe with rect
        return map_obj 
    else:
        return "unknown map"



def display_free_moving(win, pos, keys, map, global_dict, display_t=0.5,map_display=False, dim=[4,3]):
    ref_table = global_dict['position'];
    ref_symbol = global_dict['symbol'];
    if 'z' in keys:
        pos = new_position(pos,'up',map,dim=dim);
        symbol = visual.ImageStim(win=win,image=f"IMG/{ref_symbol['2']}", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,-.2*win.size[1])); 
    elif 's' in keys:
        pos = new_position(pos,'down',map,dim=dim);
        symbol = visual.ImageStim(win=win,image=f"IMG/{ref_symbol['-2']}", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,-.2*win.size[1])); 
    elif 'q' in keys:
        pos = new_position(pos,'left',map,dim=dim);
        symbol = visual.ImageStim(win=win,image=f"IMG/{ref_symbol['-1']}", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,-.2*win.size[1])); 
    elif 'd' in keys:
        pos = new_position(pos,'right',map,dim=dim);
        symbol = visual.ImageStim(win=win,image=f"IMG/{ref_symbol['1']}", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,-.2*win.size[1])); 

    room = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(pos)]}", size=(0.4*win.size[1],0.4*win.size[1]) ,pos=(0,.2*win.size[1])); 
    room.draw();
    symbol.draw();
    if map_display:
        dot = mini_map(win,pos,map,global_dict);
        dot.draw();
#    else:
#        dot = visual.Circle(win=win, radius=0.05,fillColor=None, lineColor=None,opacity=0)# Fully transparent

    win.flip();
    core.wait(display_t);

    room.draw();
    if map_display:
        dot.draw();
    win.flip();

    return pos


def drop_in(win,map,global_dict,frame,pos = None,wait=2,dim=[4,3]):
    col = global_dict['color'];
    ref_table = global_dict['position'];
    if pos is None:
        pos = np.random.randint(0,dim[0]*dim[1]);
    if frame:
        frame = visual.Rect(win,width=0.75*win.size[0], height=0.75*win.size[1], lineColor = col[map],lineWidth =0.05*win.size[1]);
        frame.draw();
        win.flip();
        core.wait(wait);
        
    room = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(pos)]}", size=(0.4*win.size[1],0.4*win.size[1]) ,pos=(0,.2*win.size[1]));
    room.draw();
    win.flip();
    
    return pos


def explo(pos,explored,dim=[4,3]):
    if pos not in explored:
        explored.append(pos);
        return False
    else:
        if len(explored)>=dim[0]*dim[1]:
            return True
        else:
            return False


def random_walk(n, moves = ['z','s','q','d'], Uturn = False):
  traj = [];
  if Uturn:
    for i in range(n):
      traj.append(np.random.choice(moves));
  else:
    opposite_moves = {'z': 's', 's': 'z', 'q': 'd', 'd': 'q'}
    
    for i in range(n):
        if traj: #Exclude the oposite move to the previous input
            allowed_moves = [move for move in moves if move != opposite_moves[traj[-1]]]
        else:
            allowed_moves = moves 
        traj.append(np.random.choice(allowed_moves))
  return traj


def feedback(win,bool,time = 0.7):
    if bool:
        fb = visual.ImageStim(win=win,image=f"IMG/Right.png", size=(0.3*win.size[1],0.3*win.size[1]) ,pos=(0,0));
    else:
        fb = visual.ImageStim(win=win,image=f"IMG/Wrong.png", size=(0.3*win.size[1],0.3*win.size[1]) ,pos=(0,0));
    
    fb.draw();
    win.flip();
    core.wait(time);


def permute(arr, start=0, result=None): #Auto-recursive function
    if result is None:
        result = [] # Initiate the combination list

    if start == len(arr) - 1:
        result.append(arr[:])  # Append a copy of the current permutation
    else:
        for i in range(start, len(arr)):
            arr[start], arr[i] = arr[i], arr[start]  # Swap elements
            permute(arr, start + 1, result)          # Recurse with result passed
            arr[start], arr[i] = arr[i], arr[start]  # Swap them back

    return result

def shortest_path(A,B,map,dim):
  '''This function minimal compute the number of action to go from A to B as function of the map'''
  if map == "circle":
    dist = min((A-B)%(dim[0]*dim[1]),-(A-B)%(dim[0]*dim[1]));
    n_move = dist//2 + dist%2

    #Paths
    if (A-B)%(dim[0]*dim[1]) < -(A-B)%(dim[0]*dim[1]): #Backward shorter than Forward
      one_path = ["down"]*(dist//2) + ["left"]*(dist%2)
    else:
      one_path = ["up"]*(dist//2) + ["right"]*(dist%2)


  elif map =="taurus":
    A_x, A_y = A%dim[1], A//dim[1];
    B_x, B_y = B%dim[1], B//dim[1];

    dist_x = min((A_x-B_x)%dim[1],-(A_x-B_x)%dim[1]);
    dist_y = min((A_y-B_y)%dim[0],-(A_y-B_y)%dim[0]);
    n_move = dist_x + dist_y
  else:
    return "Error: unknown map"
  return n_move

def test_goal(win,map,ref_table,minDist=2,dim=[4,3],max_it=100,timeAnim = .5):
    A = np.random.randint(0,dim[0]*dim[1]);
    B = np.random.randint(0,dim[0]*dim[1]);

    dist = shortest_path(A,B,map,dim);
    c = 0;
    while dist < minDist and c < max_it:
        B = np.random.randint(0,dim[0]*dim[1]);
        dist = shortest_path(A,B,map,dim);
        c+=1;
    A_im = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(A)]}", size=(0.4*win.size[1],0.4*win.size[1]) ,pos=(-0.3*win.size[0],0));
    B_im = visual.ImageStim(win=win,image=f"IMG/{ref_table[str(B)]}", size=(0.4*win.size[1],0.4*win.size[1]) ,pos=(0.3*win.size[0],0));
    arrow = visual.ImageStim(win=win,image="IMG/Right_arrow.png", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,0));

    #Animation
    A_im.draw();
    win.flip();
    core.wait(timeAnim);
    A_im.draw();
    arrow.draw();
    win.flip();
    core.wait(timeAnim);
    A_im.draw();
    arrow.draw();
    B_im.draw();
    win.flip();

    event.waitKeys(keyList=['z','s','q','d']);


    return A, B, dist
    
def start_screen(win):
    """
    Display the start panel
    """

    text = visual.TextStim(win, text="Welcome to this experiment!", color='#f5f5f5', height=0.1*win.size[1], pos=(0, 0.20*win.size[1]),wrapWidth=win.size[0]*0.8)
    text2 = visual.TextStim(win, text="Press 'space' if you are ready to start.", color='#f5f5f5', height=0.05*win.size[1], pos=(0, -0.2*win.size[1]),wrapWidth=win.size[0]*0.8)

    text.draw()
    text2.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])

    return keys


def finish_screen(win):
    """
    Display the end panel
    """
    bg = visual.ImageStim(win=win,image="IMG/Fireworks.jpg",size = win.size,pos=(0,0));
    bg.draw();

    text = visual.TextStim(win, text="Thank you for participating!", color='white', height=0.12*win.size[1], pos=(0, -0.05*win.size[1]),wrapWidth=win.size[0]*0.95)
    text2 = visual.TextStim(win, text="Press any key to exit", color='white',height=0.08*win.size[1], pos=(0, -0.3*win.size[1]),wrapWidth=win.size[0]*0.8)
    text.draw()
    text2.draw()
    
    

    win.flip()
    
    event.waitKeys()
    return 0

