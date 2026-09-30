import time
import numpy as np

import TOH.parameters as Params
from TOH.build import *


class SearchAlgorithm(object):
    
    def __init__(self,n):

         
        self.Game = Game(n)
        self.Game.create()
        self.Counter = Counter()
        self.Frontier = Frontier()

        self.initial_state = self.Game.initial_state   


class A_star(SearchAlgorithm):
    
    def __init__(self,n_disks, heuristic, pdb_inst = None):
        
        print('\n=============== Creating game ===========')
        super().__init__(n_disks)

        print(f'\nInitial state:\n{np.array(self.Game.initial_state).T[::-1]}')
        print(f'\nGoal state:\n{np.array(self.Game.goal_state).T[::-1]}')  

        self.run_time=None
        self.heuristic = heuristic

        self.Frontier.f_l = {'s':0, 'g':1, 'f':2, 's_key':3, 'ps_key':4} 
        # Sot frontier by f then g then state
        self.frontier_sort_lambda = lambda x: (x[self.Frontier.f_l['f']], x[self.Frontier.f_l['g']], x[self.Frontier.f_l['s']])
        
        if heuristic == 'pdb' and pdb_inst is None:
            m_disks = int(input('\n Enter m subset disks for PDB heuristic: '))
            self.PDB = PDB(m= m_disks)
            self.PDB.create_table()
        else:
            self.PDB = pdb_inst

        self.start_time = time.time() 


    def find_pdb_h(self, state):
        ''' 
        Mutates a state and find its pdb heuristic from the pdb table
        '''

        mut_state = self.PDB.mutate_state(state)
        node_h = [f[1] for f in self.PDB.pdb_table if f[0] == mut_state].pop()
        return node_h


    def execute(self):
        '''
        Executes a_star algorithm over n iterations
        '''
        
        # Initialise state_0 values
        if self.heuristic == 'pdb':
            node_h = self.find_pdb_h(self.initial_state)
        else:
            node_h = Heuristics(self.Game, State(self.initial_state)).heuristic(self.heuristic)
        self.Frontier.frontier.append(( self.initial_state, 0, node_h, self.Counter.state_key(), None ))
        
        print(f'\nStarting A* algorithm with heuristic : {self.heuristic}... ')
        for step in range(Params.MAX_ITER):  
            
            frontier_set = set(self.Frontier.frontier)
            frontier_states = [front[self.Frontier.f_l['s']] for front in frontier_set]
            
            if not frontier_set:
                raise RuntimeError (f'\n After {step} steps, I am a failure - no solutions found :(')
            
            # Pop best fronts by their lowest f_value
            front = self.Frontier.pop_best_front(sort_key = self.frontier_sort_lambda)
            
            # Open node
            s_key = front[self.Frontier.f_l['s_key']]
            node_state = front[self.Frontier.f_l['s']]
            node_g = front[self.Frontier.f_l['g']] 
            
            if node_state == self.Game.goal_state:
                run_secs = (time.time() - self.start_time )
                self.run_time = [int(np.floor(run_secs/60)),  round((run_secs*100) %60, 2)]
                print (f"""
                        

Wooo! Goal state reached ! 
        
*************************************
             A* complete
                       
Disks : {len(self.Game.disk_values)}
Heuristic: {self.heuristic}

Stats:
 Layers from initial state = {node_g}
 Cost = {front[self.Frontier.f_l['f']]}
 Unique states found = {self.Counter.state_counter}
 Iterations / Nodes opened = {step}
 Time elapsed = {self.run_time[0]}m {self.run_time[1]}s
 
 *************************************
                    """) 
                
                # Used for backtracing to find optimal path from closed set
                return self.Frontier.closed, front, node_g
            

            # Return child states
            child_States = State(node_state).find_child_states()
            #Explored state is now closed
            self.Frontier.closed.append(front)
            closed_set = set(self.Frontier.closed)
            closed_states = [c_front[self.Frontier.f_l['s']] for c_front in closed_set]

            for c_State in child_States:
                c_state = c_State.state
                
                # if child state in closed states or frontier states ignore else add to frontier
                if c_state in closed_states + frontier_states :
                    continue

                if self.heuristic == 'pdb':
                    c_h = self.find_pdb_h(c_state)
                else:
                    c_h = Heuristics(self.Game, c_State).heuristic(self.heuristic)
                    
                c_g = node_g + self.Game.unit_path_cost
                c_front = (c_state, c_g, c_g + c_h, self.Counter.state_key(), s_key)
                
                # if child state in frontier states but child state has a lower g(n) replace frontier state with child state
                if c_state in frontier_states :
                    front = list(frontier_set)[frontier_states.index(c_state)]
                    f_g = front[self.Frontier.f_l['g']]
                    if c_g < f_g:
                        self.Frontier.frontier.remove(front)
                        self.Frontier.frontier.append(c_front)
                    continue

                else:
                    self.Frontier.frontier.append(c_front)

                 
            
class BFS(SearchAlgorithm):

    def __init__(self,n_disks):
        
        super().__init__(n_disks)
        self.n_disks=n_disks
        self.run_time=None
        self.start_time = time.time() 
        
    def execute(self, is_pdb = None):
        '''
        Executes bfs algorithm over n iterations with modifications for running inside a PDB
        '''

        # Initialise state_0 values
        if is_pdb:
            print(f'\n=== Starting PDB with {self.n_disks} disks ===')
            self.Frontier.frontier.append(( self.Game.goal_state, 0, self.Counter.state_key(), None ))
        else:
            print('\n=============== Creating game ===========')
            print(f'\nInitial state:\n{np.array(self.Game.initial_state).T[::-1]}')
            print(f'\nGoal state:\n{np.array(self.Game.goal_state).T[::-1]}') 
            print('\nStarting BFS algorithm ... ')
            self.Frontier.frontier.append(( self.Game.initial_state, 0, self.Counter.state_key(), None ))
        
        self.Frontier.f_l = {'s':0, 'g':1, 's_key':2, 'ps_key':3}
        
        
        for step in range(Params.MAX_ITER):
            
            frontier_set = set(self.Frontier.frontier)
            frontier_states = [front[self.Frontier.f_l['s']] for front in frontier_set]
            
            if not frontier_set:
                if not is_pdb:
                    raise RuntimeError (f'\n After {step} steps, I am a failure - no solutions found :(')
                run_secs = (time.time() - self.start_time )
                self.run_time = [int(np.floor(run_secs/60)),  round((run_secs*100) %60, 2)]
                return sorted([(f[0],f[1]) for f in closed_set], key = lambda x: -x[self.Frontier.f_l['g']])
            # Pop best fronts by their lowest g_value
            front = self.Frontier.pop_best_front(sort_key = lambda x: x[self.Frontier.f_l['g']])
            
            # Open node
            s_key = front[self.Frontier.f_l['s_key']]
            node_state = front[self.Frontier.f_l['s']]
            node_g = front[self.Frontier.f_l['g']] 
            if node_state == self.Game.goal_state and not is_pdb:
                run_secs = (time.time() - self.start_time )
                self.run_time = [int(np.floor(run_secs/60)), round((run_secs*100) %60, 2)]
                print (f"""
                        

 ---- Wooo! Goal state reached ! ----

{np.array(node_state).T[::-1]}
        
*************************************
             BFS complete

Disks : {len(self.Game.disk_values)}

Stats:
 Cost / Layers from initial state = {node_g} 
 Unique states found = {self.Counter.state_counter}
 Iterations /  Nodes opened = {step}
 Time elapsed = {self.run_time[0]}m {self.run_time[1]}s
 
 *************************************
                        
                        """
                        )
                
                # Used for backtracing to find optimal path from closed set
                return self.Frontier.closed, front, node_g
                
            # Return child states
            child_States = State(node_state).find_child_states()
            #Explored state is now closed
            self.Frontier.closed.append(front)
            closed_set = set(self.Frontier.closed)
            closed_states = [c_front[self.Frontier.f_l['s']] for c_front in closed_set]

            for c_State in child_States:
                c_state = c_State.state
               
                # if child state in closed states or frontier states ignore else add to frontier
                if c_state in closed_states + frontier_states :
                    continue
                
                c_g = node_g + self.Game.unit_path_cost
                c_front = (c_state, c_g, self.Counter.state_key(), s_key)
                # if child state in frontier states but child state has a lower g(n) replace frontier state with child state
                if c_state in frontier_states :
                    front = list(frontier_set)[frontier_states.index(c_state)]
                    f_g = front[self.Frontier.f_l['g']]
                    if c_g < f_g:
                        self.Frontier.frontier.remove(front)
                        self.Frontier.frontier.append(c_front)
                    continue

                else:
                    self.Frontier.frontier.append(c_front)
                
                     

class PDB(SearchAlgorithm):
    

    def __init__(self,m):
        
        self.m = m 
        super().__init__(self.m)
        self.pdb_table = None
        self.run_time = None

    def mutate_state(self,state):
        ''' 
        Change a TOH state to a PDB state.
        '''

        mut_state = []
        
        # mutate and trim peg
        for peg in state:
            mutate_peg = [d for d in peg if d <= self.m]
            mutate_peg = mutate_peg[:self.m] # top trim state
            mut_state.append(tuple(mutate_peg))

        return tuple(mut_state)
    
    def create_table(self):
        ''' 
        Runs Breadth First Search from a mutated goal state until no fronts left
        returns a ordered by g ascending list of states.
        '''
        pdb_run = BFS(n_disks = self.m)
        self.pdb_table = pdb_run.execute(is_pdb = True)
        self.run_time = pdb_run.run_time
        return
    