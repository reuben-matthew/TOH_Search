This repo allows running of the search algorithms A* , Depth-First Search, and Breadth-First Search on the Towers of Hanoi game using a heuristic that you choose. The rules are that a larger peg cannot be placed above a smaller peg and that only 1 peg can be moved each turn.

# Running the tasks

To run the program:

```bash
cd /source 
python3 TOH_SA.py
```

Notes:
- You must rerun the program each time you want to execute a different tasks.
- The program prompts for a sequence of inputs; the tokens inside [] brackets in the prompts are the valid input options.
- The program assumes the following parameters which can be changed to any integer value > 0, if needed do so in (TOH/parameters.py) :
    MAXIMUM ITERATIONS = 10**5
    NUMBER OF PEGS = 3
    STARTING M FOR FINDING MAXIMUM M IN A PDB FOR T < 5 MINUTES = 5


## 1.1:

    - Run A* with the admissable (out-of-place) heuristic:
        `c → p → (n disks) → a_star → oop`
    - Run A* with the in-admissable (Manhattan squared distance) heuristic:
        `c → p → (n disks) → a_star → man2`
    - Run BFS:
        `c → p → (n disks) → bfs`
    - To skip printing the solution path, input `n` when prompted. Otherwise the program prints each step/state transition with a 1‑second delay.



##  1.2:

    If you would like to see the runtime table of h1,h2 for A*:

    - Select `c → r `:
        - Select starting n disks and end n disks
        - program will print runtimes. Runtime values are displayed as [ minutes, seconds ]


## Extension - 1.3:

    - Enter `e` to access extension options with the first prompt.

    1. Run A* with a PDB heuristic for n (disks) and m (subdisks)
        - Select `1` and enter the values when prompted.

    2. Build the Pattern Database (PDB)
        - Select `2` to start building the PDB. 
        - By default the build uses a subset of 6 disks (confidently presumed to finish in under 5 minutes).
            - To change this, edit  /source/TOH/parameter.py:
                - Update the variable: PDB_MAX_M_TEST_M0 and rerun the program.

    3. Finding biggest n
        - After building the PDB (bullet point 2.), when prompted select `y`.
        - If the program stops before you can press `y`, rerun and input:
            - `e → 3`
            - Then select `m` as the maximum value from which you want to build the PDB with.
            - A* will then begin to run using a PDB.

