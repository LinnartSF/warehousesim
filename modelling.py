from framework import *
from strategies import *

import random


# class for building a vehicle routing simulation model
class Model:
    """class used for modelling the vehicle interaction layout and routing

    note: Tasks, Queued, Jobs must strictly be FIFO managed
    
    """

    Grid        :Layout
    Iterations  :int
    Iteration   :int
    Vehicles    :list
    Tasks       :dict # all tasks that are not ready for dispatch yet (FIFO management)
    Queued      :list # all tasks that are ready for dispatch  (FIFO management)
    Jobs        :list # jobs are dispatched tasks, i.e. activated tasks that have already been assigned to vehicles (hence "jobs") (FIFO management)
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

        # TODO detect violations of start date FIFO management required, and place task at correct index to ensure FIFO order and management

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

        # 1: check if any tasks can be queued for dispatch
        for t in self.Tasks:
            
            if t.Startdate <= self.Iteration:

                self.Queued.append(t)
                self.Tasks.remove(t)

            else:

                break # no need to search rest of task list since FIFO management based on start date is assumed

        # 2: check if queued tasks (if any) can be released and assigned to a vehicle
        availables = [o for o in self.Vehicles if len(o.Path_edges) > 0]

        if len(availables):

            for t in self.Queued:

                # assign task to random vehicle
                # TODO implement other assignment logics

                v = random.choice(availables)

                # what is the current vehicle position? 

                # determine path to start position of job

                # 




                

        # 3: for all jobs, update cross points
        # TODO

        # 4: schedule jobs by reserving edges and nodes, and by assigning ownerships; considering cross points
        # TODO

        # 5: execute vehicle movements (where possible)
        # TODO

        # 6: any vehicle that has completed its edge enters node, if node is free
        # TODO

        # 7: update location attribute in all vehicles
        # TODO

        # 8: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle instance
        # TODO

        pass
        
        # 9: increment iteration
        self.Iteration += 1