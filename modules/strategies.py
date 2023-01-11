from framework import *
from modelling import *

import random

"""

if meaningful, strategies can be specified and accessed here

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

"""

def assign(m: Model) -> None:
    """assigns tasks registered in model to vehicles as jobs

    function checks all registered tasks in model and releases tasks to list of active jobs if vehicle available
    function also responsible for deciding which vehicle should receive the job

    Args:
        m (Model): simulation Model class instance from modelling.py module
    
    Returns:
        None
    
    """
    
    # check for jobs release, assign jobs to vehicle
    for t in m.Tasks:

        if t.Startdate > m.Iteration:

            break

        else:

            availables = [v for v in m.Vehicles if len(v.Path_edges) == 0]

            if len(availables) > 0:

                random.shuffle(availables)
            
                v = availables.pop(0)

                if type(v.Loc) == Node:

                    ref = t.Edges[0].I

                elif type(v.Loc) == Edge:

                    ref = t.Edges[0]

                if v.Loc == ref:

                    # assign job to vehicle
                    v.Job = t                               # critical
                    v.Path_edges = t.Edges                  # critical
                    v.Path_edgetimes = t.Speeds             # critical
                    t.Transporter = v                       # critical
                    m.Jobs.append(t)
                    m.Tasks.remove(t)
                
                else:

                    # add edges until task path initial
                    print("WARNING this is not implemented in test.py yet!")