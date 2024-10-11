from psychopy import visual, event, core

from NavTask_functions import *

#Constants
n_explore = 20;
training_bloc = 1;
n_test_rw = 2;
len_walk= 20;
n_test_seek = 1;
n_seek = 10;
rep_seek_samemap = 3;


global_dict = generate_references();

win = visual.Window(units='pix', fullscr=True, color='black');
MAP = ["taurus","circle"];

start_screen(win);
while True:
    ##Training
    for b in range(training_bloc):
        print(f"Training {training_bloc}:");
        #Select map order
        np.random.shuffle(MAP);
        for t in range(2):
            print(f"#{t} map: {map}");
            map = MAP[t];
            #Place the player inside the map
            pos = drop_in(win,map,global_dict,frame=True);
            #Initialize markers
            steps = 0; ex_completed = False; explored = [];
            while steps < n_explore and not ex_completed:
                keys = event.waitKeys();
                if 'escape' in keys:
                    break
                else:
                    pos = display_free_moving(win,pos,keys, map, global_dict)
                    ex_completed = explo(pos,explored);

    ##Testing
    #Test 1
    for t in range(n_test_rw):
        print(f"Testing {t} map: {map}");
        map = np.random.choice(MAP);
        #Place the player inside the map
        pos = drop_in(win,map,global_dict,frame=False); #Ofc we hide the color of the map
        #Initialize markers
        traj = random_walk(len_walk);
        bot_step=0;
        while bot_step < len_walk:
            keys = event.waitKeys(keyList=['escape','z','s','q','d'],maxWait=1);
            #Bot's walk
            pos = display_free_moving(win,pos,traj[bot_step], map, global_dict);
            if keys is not None:
                if 'escape' in keys:
                    break
                elif 'z' in keys or 's' in keys: #Taurus
                    if map == 'taurus':
                        feedback(win,True);
                        break;
                    else:
                        feedback(win,False);
                        break;
                else:#Circle
                    if map == 'circle':
                        feedback(win,True);
                        break;
                    else:
                        feedback(win,False);
                        break;
            bot_step += 1;

    #Test Seeking
    #Set the map and define the goal
    for t in range(n_test_seek):
        print(f"Seeking test #{t}");
        map = np.random.choice(MAP);
        print(map);
        retrial = 0;
        while retrial < rep_seek_samemap:
            print(f"Retrial #{retrial}, map: {map}");
            A, B, dist = test_goal(win,map,global_dict['position']);
            print(f"{A} to {B}");
            #Place the player inside the map
            pos = drop_in(win,map,global_dict,frame=True,pos=A);
            #Initialize markers
            steps = 0; path = [pos];
            while steps < n_seek and pos != B:
                keys = event.waitKeys();
                if 'escape' in keys:
                    retrial = rep_seek_samemap;
                    break
                else:
                    pos = display_free_moving(win,pos,keys, map, global_dict)
                    path.append(pos)
                    steps+=1;
            retrial +=1;

            if pos == B:
                feedback(win,True);
            else:
                feedback(win,False);
                
            print(f"Path: {path}\nDistance: {len(path)}\tminimum: {dist}");

    break

finish_screen(win);

win.close();
core.quit();