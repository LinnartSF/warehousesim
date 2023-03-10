"""

this module mainly contains the Model class
main simulation control can be implemented centrally in this module by adjusting the Model class' step()-method

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

"""

from framework import *
from ui import *

import numpy as np

import random
import copy

# class for building a vehicle routing simulation model
class Model:
    """class used for modelling the vehicle interaction layout and routing

    note: Tasks, Queued, Jobs must strictly be FIFO managed
    
    """

    Grid        :Layout
    Iterations  :int
    Iteration   :int
    Vehicles    :list
    Tasks       :list       # all tasks that are not ready for dispatch yet (FIFO management)
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

        # prepopulate animation data template 
        self.Results = None   # (col1 simtime, col2 posx (col), col3 posy (row), col4 for number of vehicles
    
    def get_edges(self, 
                  nodeseq: list
                 ) -> list:
        """returns edge indices, derived from node sequence

        this returns a list with all edges, derived from the forwarded node index sequence
        edge indices are derived from the input node sequence, and used to access and return list of related Edge object

        Args:
            nodeseq (list): sequence of nodes for which edges are to be derived (ints)
    
        Returns:
            edgeseq (list): list of derived edges

        """

        edgeidxs = []

        for i in range(0,len(nodeseq)-1):

            edgeidxs.append((nodeseq[i], nodeseq[i+1]))

        return [self.Grid.Edges[idx] for idx in edgeidxs]
    
    def add_vehicle(self,
                    id: int,
                    type: str,
                    loc: any = None # TODO check if it doesnt make more sense to locate every vehicle at one edge or node, first
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
                assignment :bool = False
                ) -> bool:
        """method for adding tasks to model
        
        should be called at the beginning after setting up model, before running model; 
        tasks should be added in sequence, in accordance with their earliest start date
        .Tasks attribute list is just a record of all tasks to be executed, and should later be turned into jobs

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
    
    def convert_task_to_job(
                            self,
                            task: Task,
                            vehicle: Vehicle
                           ) -> None:
        """converts task into active job and assigns to vehicle

        helper function that removes task from .Tasks list and adds it to active .Jobs list, and also assigns it to specified vehicle,
        if task edge list start point deviates from current vehicle, this method calcualetes the remaining edges to that start point and adds them to the path list of the job

        Args:
            task (Task):
            vehicle (Vehicle):
        
        Returns:
            None

        """

        # TODO implement
        pass
        
    def step(self) -> None:
        """implements one incremental iteration of the simulation

        should only be called once model, its tasks, and its vehicles have fully been setup;
        step()-method makes several assumptions:
        - assumes that all vehicles are managed centrally in Model class by calling step()-method (decentral implementation through step() method in Vehicle class)
        - assumes that only activated tasks are added to .Jobs list of model instance
        - every job in .Jobs list is already assigned to a vehicle

        Args:
            None
        
        Returns:
            None
        
        """

        # node: model logic currently does not make use of .Reservation attributes in Edge and Node instances

        # note: task assignment is done externally in main run routine, i.e. all jobs are 

        #############################################################################################################################################################
        # 1: update crosspoints list for new jobs
        for j in self.Jobs:

            # check if job has already been considered for crosspoint checks
            if j.CPCChecked == True: 
                
                break
            
            else: 

                # find additional cross points for every node in jobs future node list
                for n in j.Nodes_future:

                    # first, check if job should be registered at existing crosspoints
                    for cp in self.Crosspoints:

                        if n == cp.Nodeobj:
                            
                            if j not in cp.Jobs:
                                
                                cp.Jobs.append(j)

                            j.CPCChecked = True
                
                if not j.CPCChecked:

                    for n in j.Nodes_future:

                        # check every future node and find all other jobs that have this node in their future as well
                        if not j.CPCChecked:

                            for oj in self.Jobs:

                                if j == oj:

                                    pass

                                else:

                                    for on in oj.Nodes_future:

                                        if n == on: 

                                            # create crosspoint and append to .Crosspoints list attribute
                                            cp = Crosspoint(node = n, jobs = [j,oj])
                                            j.Crosspoints.append(cp)
                                            oj.Crosspoints.append(cp)
                                            self.Crosspoints.append(cp)
                                            cp.Node.Crosspoint = cp

                # remember that this job has already been checked
                j.CPCChecked = True

        #############################################################################################################################################################
        # 2: schedule jobs by reserving edges and nodes 
        # TODO implement other sequencing strategies here; default logic implemented below (without using strategies.py)
        jobs = copy.copy(self.Jobs)
        random.shuffle(jobs)       
        for j in self.Jobs:

            # check up to next crosspoint if this job can become edge owner
            if type(j.Transporter.Loc) == Edge: # VEHICLE CURRENTLY LOCATED ON EDGES

                # is target node still "reservable"? or is this vehicle already owner
                if j.Transporter.Path_edges[0].J.Capacity > len(j.Transporter.Path_edges[0].J.Owners) or j.Transporter in j.Transporter.Path_edges[0].J.Owners:

                    if j.Transporter not in j.Transporter.Path_edges[0].J.Owners: 
                    
                        # reserve node (register as owner)
                        j.Transporter.Path_edges[0].J.Owners.append(j.Transporter)
                
                    # enter a loop reserving up until end or next crosspoint
                    if j.Transporter.Path_edges[0].J.Crosspoint == None: # first node is not a crosspoint

                        # if not enter loop until crosspoint or last node and register as owner, or until capacity does no longer suffice
                        if len(j.Transporter.Path_edges) > 1:

                            for e in j.Transporter.Path_edges[1:]:
                                
                                # register as owner of edge, if applicable
                                if e.Capacity > len(e.Owners) or j.Transporter in e.Owners:

                                    if j.Transporter not in e.Owners: 
                                        
                                        e.Owners.append(j.Transporter)
                                
                                else:

                                    break

                                # register as owner of node, if applicable
                                if e.J.Capacity > len(e.J.Owners) or j.Transporter in e.J.Owners:

                                    if j.Transporter not in e.J.Owners: 
                                        
                                        e.J.Owners.append(j.Transporter)
                                
                                else:

                                    break
                                
                                # stop here if crosspoint is reached (only schedule vehicles up until crosspoints)
                                if e.J.Crosspoint == None:

                                    break
            
            else: # VEHICLE CURRENTLY HOLDING ON NODE

                for e in j.Transporter.Path_edges:
                                
                    # register as owner of edge, if applicable
                    if e.Capacity > len(e.Owners) or j.Transporter in e.Owners:

                        if j.Transporter not in e.Owners: 
                                        
                            e.Owners.append(j.Transporter)
                                
                        else:

                            break

                        # register as owner of node, if applicable
                        if e.J.Capacity > len(e.J.Owners) or j.Transporter in e.J.Owners:

                            if j.Transporter not in e.J.Owners: 
                                        
                                e.J.Owners.append(j.Transporter)
                                
                            else:

                                break
                                
                            # stop here if crosspoint is reached (only schedule vehicles up until crosspoints)
                            if e.J.Crosspoint == None:

                                break
        
        #############################################################################################################################################################
        # 3: execute vehicle movements (where possible), if vehicle is in a node it enters next edge, if edge is free: update path data; this step includes time consumption and consumes remaining edge time (if above zero)
        # TODO decentralize this step in next sprint
        for v in self.Vehicles: # TODO implement order ordering types; so far sequential order implemented here to begin with (without using strategies.py)

            # only consider "busy" vehicles
            if len(v.Path_edges) > 0:
            
                # current location is a Node?
                if type(v.Loc) == Node:

                    # is vehicle owner of next in edge path
                    if v in v.Path_edges[0].Owners:
                    
                        # no longer owner of node that is now exited by vehicle
                        if v in v.Loc.Owners: v.Loc.Owners.remove(v)

                        # update vehicle location
                        v.Loc = v.Path_edges[0]

                        # update node future and history
                        if v.Loc.I == v.Job.Nodes_future[0]: v.Job.Nodes_history.append(v.Job.Nodes_future.pop(0))

                # all vehicles that are on a edge consume one time step of remaining dwell time on edge
                if type(v.Loc) == Edge:

                    v.Path_edgetimes[0] -= 1 # consume one time step of dwell time on edge

        #############################################################################################################################################################
        # 4: any vehicle that has completed its edge enters node at edge end, if node is free; update location attribute in all vehicles
        for v in self.Vehicles: # TODO allow for different ordering strategies here, instead of same vehicle sequence every time (without using strategies.py)

            if v.Job !=None and len(v.Path_edges)>0:

                if v.Path_edgetimes[0] <= 0:

                    if v in v.Path_edges[0].J.Owners:

                        # no longer owner of edge that will now be exited
                        v.Loc.Owners.remove(v)

                        # update vehicle location to now be located in node
                        v.Loc = v.Path_edges[0].J

                        # remove old edge
                        _ = v.Path_edges.pop(0)

                        # remove therewith associated dwell time index
                        _ = v.Path_edgetimes.pop(0)

        #############################################################################################################################################################
        # 5: write vehicle location data into .Results attribute (allowing for animations lateron)
        for vi in range(0,len(self.Vehicles)):

            v = self.Vehicles[vi]

            # vehicle currently located on Node
            self.Results[self.Iteration+vi, 0] = self.Iteration + 1
            self.Results[self.Iteration+vi, 1] = v.ID

            # is current location Edge or Node type?
            if type(v.Loc) == Edge:

                # vehicle currently located on edge
                i = v.Loc.I.ID
                j = v.Loc.J.ID

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

        #############################################################################################################################################################
        # 6: check all jobs whether they have been completed; if so, pop them and make vehicle "idle" (empty Path_ lists), while mainting relevant location in location attribute of vehicle entrance
        for v in self.Vehicles:

            if v.Job:

                if len(v.Path_edges) == 0:

                    # job complete, remove task from all crosspoints that still contain it
                    for cp in v.Job.Crosspoints:

                        cp.Jobs.remove(v.Job)
                        v.Job.Crosspoints.remove(cp)
                        cp.Node.Crosspoint = None

                    # remove crosspoints that are no longer cross points
                    for cp in self.Crosspoints:

                        if len(cp.Jobs) < 2: 
                            
                            self.Crosspoints.remove(cp)
                            cp.Node.Crosspoint = None

                    # remove job from job list 
                    self.Jobs.remove(v.Job)

                    # set vehicle to "idle" (= .Job = None)
                    v.Job = None

        #############################################################################################################################################################
        # 7: increment iteration counter
        self.Iteration += 1