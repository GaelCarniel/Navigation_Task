import numpy as np
import json
from psychopy import visual, event, core

def starting_pos(dim = [4,3],sub=None):
    row, col = dim;
    mat = np.zeros([row,col]);
#    mat_inv = np.zeros([row,col]);
    #Creating the map in 2D
    for i in range(row*col):
#        mat_inv[row-1-(i//col),i%col] = i;
        mat[(i//col),i%col] = i;
#    print(mat_inv)#Only to display it the way we are used to
    if sub is None:
        row_min, row_max, col_min, col_max = 0,row-1,0,col-1;
    else:
        row_min, row_max, col_min, col_max = sub;
    
    omega = [];
    for i in range(row_min,row_max+1):
        for j in range(col_min,col_max+1):
            omega.append(mat[i,j])

    return(int(np.random.choice(omega,1)[0]));

def new_position(pos,action,dim=[4,4],sub=None):
    '''Compute the new position in a bounded world if you use sub argument it will create a subset of your world [row_min,row_max,col_min,col_max]'''
    row, col = dim;
    n_tiles = row*col;
    
    if sub is not None:
        row_min, row_max, col_min, col_max = sub;
        if not (row_min >= 0 and row_max <= row and col_min >= 0 and col_max <= col):
            return "Error: sub dimension or too wide"
    else:
        print("Else");
        row_min, row_max, col_min, col_max = 0,row-1,0,col-1;
    
    if action == 'right':
        if pos%col + 1 > col_max:
            return pos, "no_"+action
        else:
            return pos + 1, action
    elif action == 'left':
        if pos%col - 1 < col_min:
            return pos, "no_"+action
        else:
            return pos - 1, action
    elif action == 'up':
        if (pos + col)//col > row_max:
            return pos, "no_"+action
        else:
            return pos + col, action
    elif action == 'down':
        if (pos - col) < row_min:
            return pos, "no_"+action
        else:
            return pos - col, action


def display_state(win,pos,action,dict_places,dict_symbols):
    win.flip()
    core.wait(.2);
    #Symbol draw
    if action != 'None':
        print(action);
        print("no_" in action);
        if "no_" in action:
            intended_action = action[3:];
            symbol = visual.ImageStim(win=win,image=f"../IMG/{dict_symbols[intended_action]}", size=(0.2*win.size[1],0.2*win.size[1]) ,pos=(0,0));
            symbol.draw();
            impossible = visual.ImageStim(win=win,image="../IMG/Cross.png", size=(0.2*win.size[1],0.2*win.size[1]) ,pos=(0,0));
            impossible.draw();
        else:
            symbol = visual.ImageStim(win=win,image=f"../IMG/{dict_symbols[action]}", size=(0.2*win.size[1],0.2*win.size[1]) ,pos=(0,0));
            symbol.draw();
    win.flip();
    core.wait(.5);
    win.flip()
    core.wait(.2);
    #Place draw
    room = visual.ImageStim(win=win,image=f"../IMG/{dict_places[str(pos)]}", size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,0));
    room.draw()
    win.flip()

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
  '''This function minimal compute the number of action to go from A to B, and computes the possible paths'''
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

    #Paths
    if (A_y-B_y)%dim[0] < -(A_y-B_y)%dim[0]:
      if (A_x-B_x)%dim[1] < -(A_x-B_x)%dim[1]:
          one_path = ["down"]*(dist_y) + ["left"]*(dist_x)
      else:
          one_path = ["down"]*(dist_y) + ["right"]*(dist_x)
    else:
      if (A_x-B_x)%dim[1] < -(A_x-B_x)%dim[1]:
          one_path = ["up"]*(dist_y) + ["left"]*(dist_x)
      else:
          one_path = ["up"]*(dist_y) + ["right"]*(dist_x)
  else:
    return "Error: unknown map"

  paths = set(itertools.permutations(one_path, len(one_path)))

  return n_move, paths


#Get image references
with open('Input/reference.json', 'r') as file:
    json_string = file.read()
dict_places = eval(json_string)
#Get symbol references
with open('Input/symbols.json', 'r') as file:
    json_string = file.read()
dict_symbols = eval(json_string)

win = visual.Window(units='pix', fullscr=True, color='black');

action = 'None';
dim= [4,4];
sub = [0,1,0,1]; #Pour que tu es une idée zone rouge
sub2 = [1,2,1,2]; #zone bleue
sub3 = [0,2,1,2]; #zone verte

pos = starting_pos(dim,sub);
while True:
    print(pos)
    text = visual.TextStim(win, text=pos,color="white", height=.08*win.size[1],pos=(0,0.4*win.size[1]));
    text.draw();
    win.flip();
    
    display_state(win,pos,action,dict_places,dict_symbols);
    
    keys = event.waitKeys();
    if 'escape' in keys:
        break
    elif 'z' in keys:
        pos, action = new_position(pos,'up',dim=dim,sub=sub);
    elif 's' in keys:
        pos, action = new_position(pos,'down',dim=dim,sub=sub);
    elif 'q' in keys:
        pos, action = new_position(pos,'left',dim=dim,sub=sub);
    elif 'd' in keys:
        pos, action = new_position(pos,'right',dim=dim,sub=sub);


win.close();
core.quit();
