"""

this module is used for implementing test model, test simulation, and test animations
use this script as a template for package / api consumption

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

"""

from modelling import *
from framework import *
from strategies import *
from ui import *
from animator import *

# model setup
m = Model(
            iterations = 1000, 
            rows = 30,
            columns = 30
        )

# add vehicle park
_ = [m.add_vehicle(i,"agv") for i in range(3)]

# register tasks
# TODO

# main routine (simulation)
while m.Iteration < m.Iterations:

    # check for jobs release, assign jobs to vehicles etc
    # TODO

    # simulate one step
    m.step()

# produce animation
anim_vehicles(
                model = m,
                filepath = "testvideo"
            )