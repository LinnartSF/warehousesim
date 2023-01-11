"""

this module is used for implementing test model, test simulation, and test animations
use this script as a template for package / api consumption

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

"""

from modelling import *
from framework import *
from ui import *
from animator import *

import random
import copy

import strategies as s
import util as u

# model setup
m = Model(
            iterations = 50, 
            rows = 30,
            columns = 30
        )

# add vehicles
m.add_vehicle(
    id = 1,
    type = "agv", 
    loc = m.Grid.Nodes[1]
)

# register task (note: tasks should be appended in startdate order)
m.add_task(
    startdate = 10, 
    duedate = 23, 
    type = "agv", 
    edges = m.get_edges((1,2,3,4,5,6,7,8,38,68,67)),
    speeds = [2,2,2,2,1,3,2,1,1,1,2]
)

# main routine (simulation)
while m.Iteration < m.Iterations:

    # check for jobs release, assign jobs to vehicle
    s.assign(m)

    # simulate step
    m.step()

# testing
print(m.Results)

# produce animation
anim_vehicles(
                model = m,
                filepath = "testvideo",
                fps = 1
            )