import numpy as np
import time

from TOH.speak import goodbye

def num_disks():
    while True:
        a = int(input('\nHow many disks [ 1 - n ] ? : '))
        if type(a) != int:
            print('\n * Invalid response, try again')
            continue
        else:
            return a 

def choose_task():

    while True:

        print('\nWhich tasks do you want to run :\n')
        print(' Core = [c]\n  or\n Extension = [e]')
        a = str(input('\n : '))

        if a not in ['c','e']:
            print('\n * Invalid response, try again')
            continue

        elif a == 'c' :
            while True:
                print('\nWhich Core tasks \n')
                print(' Programming = [p] \n  or\n Report = [r]')
                a = str(input('\n : '))

                if a not in ['p','r']:
                    print('\n * Invalid response, try again')
                    continue

                elif a == 'p':
                    return 'c_p'
                
                else:
                    return 'c_r'
        else:
            return a
        

def choose_search():
    while True:
        print('\nChoose Search Algorithms: [a_star, bfs]')
        a = str(input('\n : '))
        if a not in ['a_star','bfs']:
            print('\n * Invalid response, try again')
            continue
        else:
            return a  
        
        
def choose_heuristic(report = False):

    if report == True:

        h1 = 'oop'
        h2 = 'man2'
        return h1,h2  
    
    else:
        while True:
            print('\nChoose Heuristic: [oop, man, man2]')
            a = str(input('\n : '))
            if a not in ['oop','man','man2']:
                print('\n * Invalid response, try again')
                continue
            else:
                return a 

def choose_extension_programming():

    while True:
        print('\nChoose Extension Programming Tasks :\n')
        print('\n Run A* with a PDB heuristic = [1]\n  or\n Find biggest m for runtime < 5 mins = [2]\n  or\n Use biggest m and find largest n for runtime < 10 mins = [3]')
        a = int(input('\n : '))
        if a not in [1,2,3]:
            print('\n * Invalid response, try again')
            continue
        return a     
            
def extension_2to3():

    while True:
        print('\nMaximum m found, use this to find biggest n for runtime < 10 mins ? [y,n]')
        a = str(input('\n : '))
        if a == 'y' :
            return 
        elif a == 'n':
            goodbye()
        else:
            print('\n * Invalid response, try again')
            continue
          


def solution (closed_set, goal_front, goal_node_g, fl):
    
    while True:
        print('\nPrint solution ? [y,n] :')
        a = str(input('\n : '))

        if a not in ['y','n']:
            print('\n * Invalid response, try again')
            continue

        elif a == 'n':
            goodbye()

        else:
            opt_states = []

            goal_ps_key = goal_front[fl['ps_key']]
            goal_state = goal_front[fl['s']]
            opt_states.append(goal_state)

            goal_parent_front = [c for c in closed_set if c[fl['s_key']] == goal_ps_key].pop()
            goal_parent_state = goal_parent_front[fl['s']]
            opt_states.append(goal_parent_state)

            f = goal_parent_front
            for layers in range(goal_node_g-1): 
                ps_key = f[fl['ps_key']]
                parent_front = [c for c in closed_set if c[fl['s_key']] == ps_key].pop()
                parent_state= parent_front[fl['s']]
                opt_states.append(parent_state)
                f = parent_front

            for step,state in enumerate(opt_states[::-1]):
                print (f'\n --- Step {step} ---\n{np.array(state).T[::-1]}\n')
                time.sleep(1)

            return
