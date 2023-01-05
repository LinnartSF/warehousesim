from framework import *
from strategies import *
from ui import *

import numpy as np

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
    Tasks       :dict       # all tasks that are not ready for dispatch yet (FIFO management)
    Jobs        :list       # jobs are dispatched tasks, i.e. activated tasks that have already been assigned to vehicles (hence "jobs") (FIFO management)
    Crosspoints :list       # list of crosspoints in the model
    Results     :np.ndarray # container for animation, should contain animation for every iteration, for every vehicle, with columns simtime,vehiclename,xpos,ypos (4 columns)

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
        
        self.Iteration = 0   # iterations are counted starting at 0

        self.Vehicles = []   # vehicles must be added lateron by calling add_vehicle method
        self.Tasks = []
        self.Jobs = []
        self.Crosspoints = []

        self.Grid = Layout(columns, rows, nodecapacity, edgecapacity)

        # prepopulate animation data template (col1 for simulation time, col2 for vehicle position col (x), col3 for vehicle position row (y), col4 for number of vehicles
        self.Results = None   # create predefined ndarray with numpy for every vehicle added
    
    def add_vehicle(self,
                    id: int,
                    type: str,
                    loc: Edge = None # TODO check if it doesnt make more sense to locate every vehicle at one edge, first
                   ) -> None:
        """
        
        """

        o = Vehicle(id, type)

        o.Loc = loc
        self.Vehicles.append(o)

        self.Results = np.zeros(shape = (self.Iterations*len(self.Vehicles), 4))
    
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
            if j.CPCChecked == True: 
                
                break
            
            else: 
            
                # find additional crosspoints and add to model list
                # TODO extract list of nodes in this jobs path

                # append crosspoints to job, i.e. j.Crosspoints
                # TODO

                # TODO solve issue of currently not knowing if crosspoint is still relevant, might be in the past of a job, and in the future of another
                # --> TODO add to job attributes and methods for updating past and future nodes, and update these in the vehicle movement section

                # remember that this job has already been checked
                j.CPCChecked = True

        # 2: schedule jobs by reserving edges and nodes, and by assigning ownerships; considering cross points
        # TODO

        # 3: execute vehicle movements (where possible), if vehicle is in a node it enters next edge, if edge is free: update path data; this step includes time consumption and consumes remaining edge time (if above zero)
        # TODO decentralize this step in next sprint
        for v in self.Vehicles: # TODO implement order ordering types; so far sequential order implemented here to begin with

            # current location is a Node?
            if type(v.Loc) == Node:

                # is vehicle owner of next edge in path?
                if v in v.Path_edges[0]:

                    # update vehicle location
                    v.Loc = v.Path_edges[0]

            # all vehicles that are on a edge consume one time step of remaining dwell time on edge
            if type(v.Loc) == Edge:

                v.Path_edgetimes -= 1 # consume one time step of dwell time on edge

        # 4: any vehicle that has completed its edge enters node at edge end, if node is free; update location attribute in all vehicles
        for v in self.Vehicles: # TODO allow for different ordering strategies here, instead of same vehicle sequence every time

            if v.Job:

                if v.Path_edgetimes[0] <= 0:

                    if v in v.Path_edges[0].J.Owners:

                        # update vehicle location to now be located in node
                        v.Loc = v.Path_edges[0].J

                        # remove old edge
                        _ = v.Path_edges.pop(0)

                        # remove therewith associated dwell time index
                        _ = v.Path_edgetimes.pop(0)

        # 5: write vehicle location data into layout
        for vi in range(0,len(self.Vehicles)):

            v = self.Vehicles[vi]

            # vehicle currently located on Node
            self.Results[self.Iteration+vi, 0] = self.Iteration + 1
            self.Results[self.Iteration+vi, 1] = v.ID

            # is current location Edge or Node type?
            if type(v.Loc) == Edge:

                # vehicle currently located on edge
                i = v.Loc.I.ID
                j = v.Lov.J.ID

                x_i = i//self.Grid.Y + 1
                x_j = j//self.Grid.Y + 1
                y_i = i%self.Grid.Y 
                y_j = j%self.Grid.Y

                if j == i+1:     # one step downward
                    
                    self.Results[self.Iteration+vi, 2] =  x_i        # col
                    self.Results[self.Iteration+vi, 3] = 2*y_i       # row
                
                elif j == i-1:    # one step upward
                    
                    self.Results[self.Iteration+vi, 2] = x_i         # col
                    self.Results[self.Iteration+vi, 3] = (y_i-1)*2   # row
                
                elif j > i:       # step sideward to the right
                    
                    self.Results[self.Iteration+vi, 2] = 2*x_i       # col
                    self.Results[self.Iteration+vi, 3] = y_i         # row

                else:             # step sideward to the left
                    
                    self.Results[self.Iteration+vi, 2] = 2*(x_i-1)   # col
                    self.Results[self.Iteration+vi, 3] = y_i         # row

            else:

                # vehicle currently located on Node
                x_i = v.Loc.ID//self.Grid.Y 
                y_i = v.Loc.ID%self.Grid.Y 

                self.Results[self.Iteration+vi, 2] = x_i*2-1         # col
                self.Results[self.Iteration+vi, 3] = y_i*2-1         # row

        # 6: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle entrance
        for v in self.Vehicles:

            if v.Job:

                if len(v.Path_edges) == 0:

                    # job complete, remove task from all crosspoints that still contain it
                    for cp in v.Job.Crosspoints:

                        cp.Jobs.remove(v.Job)
                        v.Job.Crosspoints.remove(cp)

                    # remove crosspoints that are no longer cross points
                    for cp in self.Crosspoints:

                        if len(cp.Jobs) < 2: self.Crosspoints.remove(cp)

                    # remove job from job list 
                    self.Jobs.remove(v.Job)

                    # set vehicle to "idle" (= .Job = None)
                    v.Job = None

        # 7: increment iteration counter
        self.Iteration += 1