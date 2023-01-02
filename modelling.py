from framework import *
from strategies import *

import random

# class for building a vehicle routing simulation model
class Model:

    Grid        :Layout
    Iterations  :int
    Iteration   :int
    Vehicles    :list
    Tasks       :dict # all tasks that are not ready for dispatch yet
    Queued      :list # all tasks that are ready for dispatch 
    Jobs        :list # jobs are dispatched tasks, i.e. activated tasks that have already been assigned to vehicles (hence "jobs")
    Crosspoints :list

    def __init__(self,
                 iterations :int,
                 rows :int,
                 columns :int,
                 nodecapacity :int = 1,
                 edgecapacity :int = 1
                ):
        """Model constructor

        it is assumed that tasks are added to .Tasks attribute (list) by main program, in accordance to task dispatch:
        task dispatch control (releasing tasks) is assumed to be externally controlled

        Args: 
            iterations (int): maximum simulation runt time
            rows (int): refer to grid size in y-dimension
            columns (int): refers to grid size in x-dimension
            nodecapacity (int): maximum number of vehicles that can be in any node of the model
            edgecapacity (int): maximum number of vehicles that can be in any edge before it is "fully occupied"

        Returns:
            None 
        
        """

        self.Iterations = iterations
        
        self.Iteration = 0

        self.Vehicles = []
        self.Tasks = []
        self.Queued = []
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

        # 1: check if tasks (if any) can be released and assigned to a vehicle
        # TODO
        availables = [o for o in self.Vehicles if len(o.Path_edges) > 0]

        if len(availables):

            for t in self.Tasks:

                # 



                

        # 2: for all jobs, update cross points
        # TODO

        # 3: schedule jobs by reserving edges and nodes, and by assigning ownerships; considering cross points
        # TODO

        # 4: execute vehicle movements (where possible)
        # TODO

        # 5: any vehicle that has completed its edge enters node, if node is free
        # TODO

        # 6: update location attribute in all vehicles
        # TODO

        # 6: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle instance
        # TODO

        pass