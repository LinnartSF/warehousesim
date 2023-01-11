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

import strategies

# model setup
m = Model(
            iterations = 1000, 
            rows = 30,
            columns = 30
        )

# add vehicles
nodes = copy.copy(m.Grid.Nodes)
random.shuffle(nodes)

m.add_vehicle(
    id = 1,
    type = "agv", 
    loc = nodes[1]
)

m.add_vehicle(
    id = 2,
    type = "agv",
    loc = nodes[21]
)

m.add_vehicle(
    id = 3,
    type = "agv",
    loc = nodes[9]
)


# register task (note: tasks should be appended in startdate order)
m.add_task(
    startdate = 1, 
    duedate = 23, 
    type = "agv", 
    edges = m.Grid.Edges[(1,2),(2,3),(3,4),(4,5)], 
    speeds = [2,2,2,2]
)

m.add_task(
    startdate = 3,
    duedate = 27,
    type = "agv",
    edges = m.Grid.Edges[(21,23),(23,24),(24,25),(25,26)],
    speeds = [1,1,3,3]
)

m.add_task(
    startdate = 5,
    duedate = 50,
    type = "agv",
    edges = m.Grid.Edges[(9,10),(10,11),(11,12),(12,13)],
    speeds = [1,1,3,3]
)

# main routine (simulation)
while m.Iteration < m.Iterations:

    # check for jobs release, assign jobs to vehicle
    strategies.assign(m)

    # simulate one step
    m.step()

# produce animation
anim_vehicles(
                model = m,
                filepath = "testvideo"
            )