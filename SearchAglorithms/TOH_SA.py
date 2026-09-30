import TOH.ask as Ask
import TOH.speak as Speak
import TOH.tasks as Tasks

from TOH.parameters import *
from TOH.build import *
from TOH.algorithms import *


if __name__ == '__main__':
    Speak.welcome(MAX_ITER, NUM_PEGS)

    task = Ask.choose_task()

    if task == 'c_p':
        Tasks.core_programming()
    elif task == 'c_r':
        Tasks.core_report()
    else:
        Tasks.extension_programming()

