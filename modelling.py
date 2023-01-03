from framework import *
from strategies import *
from ui import *

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
                speeds :list, 
                assignment :bool
                ) -> bool:
        """method for adding tasks to model
        
        should be called at the beginning after setting up model, before running model; 
        tasks should be added in sequence, in accordance with their earliest start date

        Args:
            startdate (int): earliest time this job can move
            duedate (int): due date for job (arrival at sink node)
            type (str): vehicle type, if not identified all vehicle types are considered
            edges (list): edges of the job specifying the movement
            speeds (list): movement duration along every edge
            assignment (bool): specifies whether assignment to vehicle should be done by model (internally) or by main routine (externally)
        
        Returns:
            assigned (bool): True if task already assigned to vehicle, False if this has to be done externally

        """

        # TODO detect violations of start date FIFO management required, and place task at correct index to ensure FIFO order management
        if assignment == True:

            # TODO implement: 1) find vehicle in vehicle pool, 2) assign vehicle to it, 3) assign task to vehicle, 4) add assigned task directly to .Jobs list 
            warn("internal task assignment not implemented into modelling.py yet")
            return False # TODO: set True when assignment logic has been implemented
    
        else:

            self.Tasks.append(Task(startdate,
                 duedate,
                 type,
                 edges,
                 speeds
                 ))
            
            return False
        
    def step(self) -> None:
        """implements one incremental iteration of the simulation

        should only be called once model, its tasks, and its vehicles have fully been setup;
        assumes that all vehicles are

        Args:
            None
        
        Returns:
            None
        
        """

        # note: task assignment is done externally in main run routine

        # 1: update crosspoints list for new jobs
        for j in self.Jobs:

            # check if job has already been considered for crosspoint checks
            if j.CPCChecked == True: break

            # find additional crosspoints and add to model list, if any
            # TODO

            # append crosspoints to job, i.e. j.Crosspoints
            # TODO

            # remember that this job has already been checked
            j.CPCChecked = True

        # 2: schedule jobs by reserving edges and nodes, and by assigning ownerships; considering cross points
        # TODO

        # 3: execute vehicle movements (where possible)
        # TODO

        # 4: any vehicle that has completed its edge enters node, if node is free
        # TODO

        # 5: update location attribute in all vehicles
        # TODO

        # 6: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle instance
        # TODO

        pass
        
        # 8: increment iteration
        self.Iteration += 1