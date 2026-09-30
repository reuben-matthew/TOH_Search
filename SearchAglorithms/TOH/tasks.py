import pandas as pd
import time

import TOH.ask as Ask
import TOH.parameters as Params

from TOH.speak import goodbye
from TOH.algorithms import A_star, BFS, PDB

def core_programming ():
    '''
    Runs A* or BFS
    '''

    num_disks = Ask.num_disks()
    s_a = Ask.choose_search()

    if s_a == 'a_star':
        h = Ask.choose_heuristic()
        Search_A = A_star(n_disks = num_disks, heuristic=h)
        closed_set, goal_front, goal_node_g = Search_A.execute()
        fl = Search_A.Frontier.f_l

    elif s_a == 'bfs':
        Search_A = BFS(n_disks = num_disks)
        closed_set, goal_front, goal_node_g = Search_A.execute()
        fl = Search_A.Frontier.f_l

    Ask.solution(closed_set, goal_front, goal_node_g, fl)

    goodbye()
    return


def core_report():
    '''
    Run 2 heuristic for A* and runs BFS for n - n' disks
    prints a pd Dataframe of runtimes with disks
    '''

    num_disks = Ask.num_disks()
    iterations = int(input(' Till how many disks [ n - n\' ] ? : '))
    n = []
    h1_t = []
    h2_t = []
    bfs_t = []
    for disks in range (num_disks, iterations+1):
        d = disks
        n.append(d)

        h1,h2 = Ask.choose_heuristic(report = True)

        Search_A = A_star(n_disks = d, heuristic=h1)
        Search_A.execute()
        #r_a1 = Search_A.run_time
        h1_t.append(Search_A.run_time)

        Search_A = A_star(n_disks = d, heuristic=h2)
        Search_A.execute()
        #r_a2 = Search_A.run_time
        h2_t.append(Search_A.run_time)

        Search_A = BFS(n_disks = d)
        Search_A.execute()
        #r_bfs =Search_A.run_time
        bfs_t.append(Search_A.run_time)

    print('\n\nAll algorithms finished:')

    df = pd.DataFrame({'n': n , 'A*_h1': h1_t, 'A*_h2':h2_t, 'BFS':bfs_t})
    print(df)
    goodbye()
    return

def extension_programming():
    '''
    Runs PDB
    '''
    a = Ask.choose_extension_programming()
    if a == 1:
        num_disks = Ask.num_disks()

        Search_A = A_star(n_disks = num_disks, heuristic='pdb')
        closed_set, goal_front, goal_node_g = Search_A.execute()
        fl = Search_A.Frontier.f_l

        Ask.solution(closed_set, goal_front, goal_node_g, fl)
        return

    if a == 2 :
        max_disks = Params.PDB_MAX_M_TEST_M0 # Can reliably say  n = 6 takes < 5mins
        print(f'\nStarting from m = {max_disks}')
        for test in range(Params.MAX_ITER):
            PDB_ext = PDB(m= max_disks+1)
            PDB_ext.create_table()
            run_mins, run_secs = PDB_ext.run_time

            if run_mins < 5:
                print(f'\n- For m = {max_disks+1} , time = {run_mins}m {run_secs}s') 
                max_disks += 1
                continue

            else:

                print(f'\n*** PDB time limit of 5 mins exceeded *** \n\n   - time = {run_mins}m {run_secs}s for \'disks\' = {max_disks+1}\n   - Maximum m = {max_disks}')
                Ask.extension_2to3()

                PDB_ext = PDB(m= max_disks)
                PDB_ext.create_table()

                num_disks = max_disks + 1
                print(f'\n - Starting A* search using pdb table for m = {max_disks} and n = {num_disks}')
                start_time = time.time()
                for a_tests in range(Params.MAX_ITER):
                    A_run = A_star(n_disks=num_disks, heuristic='pdb', pdb_inst=PDB_ext)
                    _, __, ___ = A_run.execute()
                    run_secs = (time.time() - start_time )
                    if run_secs < (10 * 60 ):
                        print(f'\n- For n = {num_disks} , time = {int(run_secs/60)}m {round(run_secs%60,2)}s')
                        num_disks += 1
                        continue
                    else:
                        print(f'*** A* time limit of 10 mins exceeded ***\n Maximum n = {num_disks -1 }\n n = {num_disks} completed in time = {int(run_secs/60)}m {round(run_secs%60,2)}s')
                        print('\n\n Goodbye - hope you enjoyed the game :)')
                        goodbye()
                
                
    else: 

        max_m = int(input(f'\nWhat m do you want to set for the PDB ? [ 1 - m ] : '))
        PDB_ext = PDB(m= max_m)
        PDB_ext.create_table()

        num_disks = max_m + 1
        print(f'\n - Starting A* search using pdb table for m = {max_m} and n = {num_disks}')
        start_time = time.time()
        for a_tests in range(Params.MAX_ITER):
            A_run = A_star(n_disks=num_disks, heuristic='pdb', pdb_inst=PDB_ext)
            _, __, ___ = A_run.execute()
            run_secs = (time.time() - start_time )
            if run_secs < (10 * 60 ):
                print(f'\n- For n = {num_disks} , time = {int(run_secs/60)}m {round(run_secs%60,2)}s')
                num_disks += 1
                continue
            else:
                print(f'*** A* time limit of 10 mins exceeded ***\n Maximum n = {num_disks -1 }\n n = {num_disks} completed intime = {int(run_secs/60)}m {round(run_secs%60,2)}s')
                print('\n\n Goodbye - hope you enjoyed the game :)')
                goodbye()

                

               
