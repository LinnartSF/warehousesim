"""

this module contains pre-defined visualization and animation functions that can be consumed by main routine

"""

from modelling import *

import matplotlib.pyplot as plt
from celluloid import Camera
from matplotlib.ticker import MaxNLocator

import numpy as np

def anim_vehicles(
                  model :Model,
                  filepath :str,
                  fps :int = 50
                ) -> None:
    """animates vehicle simulation from start to end time 

    function for animating vehicle moved based on simulation results;
    the entire simulation run will be animated, as registered in the model's .Results attribute

    Args:
        model (Model): simulation model reference that contains simulation results
        filepath (str): where to save animation video
        fps (int): frames per second; defaults to 50 frames per second
    
    Returns:
        None
    
    """

    # setup figure
    fig = plt.figure()
    camera = Camera(fig)
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # setup axis, labels, titles
    plt.title("Vehicle simulation")
    plt.xlabel("Width")
    plt.ylabel("Length")

    # animation
    for t in range(1,model.Iterations+1):

        data = model.Results[model.Results[:,0]==t,:]
        i = data[:, 1] # vehicle ids
        x = data[:, 2] # vehicle x positions
        y = data[:, 3] # vehicle y positions

        # TODO category-based marker color

        plt.scatter(x = x,
                    y = y
        )

        if t == 1: plt.legend(loc="upper right")

        camera.snap()

    animation = camera.animate()

    animation.save(filepath+".gif", writer='PillowWriter', fps=fps)

# TODO add additional animation and visualization options