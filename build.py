import numpy as np 

import TOH.parameters as Params


class Counter(object):
    ''' 
    Used to create state counter key and track # of state expansion
    '''

    def __init__(self):

        self.state_counter = 0
    
    def state_key(self):
        key = 's_' + str(self.state_counter)
        self.state_counter += 1
        return key

class Game(object):
    ''' 
    Creates the properties of the Game instance
    '''

    TOH_n_disks = None

    def __init__(self,num_disks):

        self.n_disks = num_disks
        self.unit_path_cost = 1
        self.initial_state = ()
        self.goal_state=()
        self.goal_disks_slot = {}
        self.disk_values = None
        

    def create(self):
        
        if not self.__class__.TOH_n_disks:
            self.__class__.TOH_n_disks = self.n_disks


        self.disk_values=tuple([i for i in range(1,self.n_disks+1)])
        
        for disk in self.disk_values:
            self.goal_disks_slot[disk] = [Params.NUM_PEGS - 1, self.n_disks - disk] 
        
        i_state = []
        g_state = []
        for pid in range(Params.NUM_PEGS):
            if pid == 0:
                i_state.append(self.disk_values[::-1]) 
                g_state.append(tuple(np.zeros(self.n_disks,int)))
                
            elif pid == Params.NUM_PEGS - 1:
                i_state.append(tuple(np.zeros(self.n_disks,int)))
                g_state.append(self.disk_values[::-1])
            else:  
                i_state.append(tuple(np.zeros(self.n_disks,int)))
                g_state.append(tuple(np.zeros(self.n_disks,int)))

        self.initial_state = tuple(i_state)
        self.goal_state = tuple(g_state)



class State(object):
    
    def __init__(self, state):
        self.state = state

    
    def free_slots(self):
        '''
        Finds the coordinates of free slots for a state
        '''

        slot_coords = []
        for pid, peg in enumerate(self.state):
            if 0 in peg:
                slot_coords.append([pid, peg.index(0)])
        
        return slot_coords


    def disk_coordinates(self, disk):
        '''
        Finds a disk peg and row index  of a state given its disk value 
        '''

        for peg_id,peg in enumerate(self.state):
            if disk in peg:
                return [peg_id,peg.index(disk)]
        
        raise ValueError(f'\nUnable to find \nDisk: {disk} \nin \nState: {self.state}')
          
    
    def movable_disks(self):
        '''
        Finds which disks can be moved
        '''

        disks = []
        for disk in [d for peg in self.state for d in peg if d!=0]:
            if self.is_top_disk(disk):
                disks.append(disk)
        return disks
     
    
    def is_top_disk(self,disk):
       ''' 
       Checks if any disks are above
       '''
       
       peg, row = self.disk_coordinates(disk)
       # Top disks = no disks above excluding 0s
       above_disks = [ d for d in self.state[peg][row+1:] if d != 0]

       return not any(above_disks) 


    def is_valid_move(self, disk, coord):
        ''' 
        Checks if any smaller disks are below for a slot to  move into
        '''

        peg, row = coord
        below_disks = self.state[peg][:row]
        
        smaller_below_disks = [ d for d in below_disks if d <= disk] # includes itself, cannot move above itself
        
        if any(smaller_below_disks):
                    return False
        
        return True
        
        
    def paths(self,disks):
        '''
        Finds legal actions of a disk
        '''

        paths=[]
        for disk in disks:
            slots = self.free_slots()
            for slot in slots: 
                if self.is_valid_move(disk, slot):
                    paths.append([disk,slot])
                
        return paths
    

    def find_child_states(self):
        '''
        Performs disk moves for each path
        '''

        child_states=[]
        disks = self.movable_disks()
        paths = self.paths(disks)
        
        for path in paths:

            disk,coord = path
            # find parent state disk location clone and mutate, set to 0 for child_state
            d_peg,d_row = self.disk_coordinates(disk)

            # change to list to mutate
            child_state = [list(peg) for peg in self.state]
            child_state[d_peg][d_row]=0
            
            # parent's path coord = disk
            n_peg, n_row =coord
            child_state[n_peg][n_row] = disk
            
            # change back to tuple for immut/hash -ability
            child_state = tuple([tuple(peg) for peg in child_state])
            
            c_State = State(child_state)
            child_states.append(c_State)
            
        return child_states
    

class Frontier(object):
    
    def __init__(self):

        self.frontier = []
        self.closed=[]
        self.f_l = None

    def pop_best_front(self, sort_key):
        ''' 
        Sorts frontier by a lambda sort key and pops first item
        '''
        
        if not self.frontier:
            raise RuntimeError (f'\nThere are no more fronts to explore \nFrontier: {self.frontier}')

        self.frontier = sorted(self.frontier, key = sort_key)
        return(self.frontier.pop(0))
    


class Heuristics(object):
    '''
    Heuristic calculations
    '''

    def __init__(self,game_inst, state_inst):
        
        self.Game = game_inst
        self.State = state_inst
    
                              
    def out_of_place(self):
        '''
        Number of pegs out of place i.e number of 0s in goal peg
        '''
        return self.State.state[-1].count(0)
        
    
    def manhattan(self,order = None):
        '''
        Sum of cardinal distances between x coordinates and y coordinates for each disk in a state
        '''
        
        sum_dist = 0
        for disk in self.Game.disk_values:
            disk_coords = np.array(self.State.disk_coordinates(disk))
            dist_x = abs(disk_coords[0] - self.Game.goal_disks_slot[disk][0])
            dist_y = abs(disk_coords[1] - self.Game.goal_disks_slot[disk][1])
            
            sum_dist += dist_x + dist_y

        if not order:
            return int(sum_dist)
        else :
            return int(sum_dist**order)
    
    
    def heuristic(self,heuristic):
        '''
        Finds the heuristic of a state
        '''
        
        if heuristic == 'oop':
            return self.out_of_place()
        elif heuristic == 'man':
            return self.manhattan()
        
        elif heuristic == 'man2':
            return self.manhattan(order=2)
        else:
            raise ValueError(f' Invalid heuristic: "{heuristic}" ')