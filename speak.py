import sys


def welcome(iter,pegs):

    print('\=============================================================================\n\n')
    print('              Welcome to the 3-peg Towers of Hanoi Search Problem !\n\n')
    print('                 Starting Parameters :')
    print(f'                                      Max iterations = {iter:,}')
    print(f'                                      Number of Pegs = {pegs}\n') 
    print('                 Search Algorithms : ')
    print('                                     A star = \'a_star\'')
    print('                                     Breadth First Search = \'bfs\'\n')
    print('                 Heuristics :')
    print('                             Out of place = \'oop\'')
    print('                             Manhattan distance = \'man\'')
    print('                             Manhattan squared distance = \'man2\'\n\n')
    print('                      |                |                |                        ')
    print('                      |                |                |                        ') 
    print('                      |                |                |                        ') 
    print('                      |                |                |                        ')
    print('                  ____|____        ____|____        ____|____                    ')
    print('                                                                                 ')
    print('==============================================================================\n\n')
    return

def goodbye():

    print('\n\n=====================================\n\n')
    print('.  Thanks for playing :)')
    print('\n\n=====================================\n\n')
    sys.exit()
    return

