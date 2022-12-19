from framework import *
from strategies import *

import random

class Model:

    Grid        :Layout
    Iterations  :int
    Iteration   :int
    Vehicles    :list
    Tasks       :list
    Jobs        :list # jobs are dispatched tasks, i.e. activated tasks that have already been assigned to vehicles (hence "jobs")
    Crosspoints :list

    def __init__(self,
                 iterations :int,
                 rows :int,
                 columns :int,
                 nodecapacity :int = 1,
                 edgecapacity :int = 1
                ):
        """
        
        """

        self.Iterations = iterations
        
        self.Iteration = 0

        self.Vehicles = []
        self.Tasks = []
        self.Jobs = []
        self.Crosspoints = []

        self.Grid = Layout(columns, rows, nodecapacity, edgecapacity)
    
    def add_vehicle(self,
                    type: str,
                    loc: Edge = None
                   ) -> None:
        """
        
        """

        o = Vehicle(type)

        o.Loc = loc

        self.Vehicles.append(o)
    
    def add_task(self,
                startdate :int,
                duedate :int,
                type :str,
                edges :list,
                speeds :list
                ) -> None:
        """
        
        should be called at the beginning after setting up model, before running model; 
        tasks should be added in sequence, in accordance with their earliest start date

        """

        self.Tasks.append(Task(startdate,
                 duedate,
                 type,
                 edges,
                 speeds
                 ))
        
    def step(self) -> None:
        """implements one incremental iteration of the simulation

        should only be called once model, its tasks, and its vehicles have fully been setup
        
        """

        # TODO implement below simulation progress logic

        # 1: check if tasks can be released and assigned to a vehicle

        # 2: for all jobs, update cross points

        # 3: schedule jobs by reserving edges and nodes, and by assigning ownerships; considering cross points

        # 4: execute vehicle movements (where possible)

        # 5: any vehicle that has completed its edge enters node, if node is free

        # 6: update location attribute in all vehicles

        # 6: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle instance

        pass