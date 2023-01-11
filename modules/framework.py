"""

module provides a library of predefined object classes
module can be consumed for simulation modelling

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

"""


# class for modeling nodes
class Node:
    """
    
    """

    Reservations :int
    Capacity     :int  # number of agvs that can fit into node
    Owners       :list # list of vehicles that reserved this node and "own" it
    ID           :int  # node index
    Crosspoint   :any  # linked crosspoint reference, if node is crosspoint (otherwise None)

    def __init__(self,
                 id : int,
                 capacity :int = 1,
                 owners :list = []
                ):
        """
        
        """

        self.ID = id
        self.Capacity = capacity
        self.Owners = owners
        
        self.Crosspoint = None

# class for modeling (one directional) edge
class Edge:
    """
    
    """

    I :Node
    J :Node
    Reservations :int
    Capacity     :int  # number of agvs that can be hosted by edge
    Owners       :list # list of vehicles allowed to operate this segment (vehicles that reserved this part)

    def __init__(self,
                 i :int, 
                 j :int,
                 capacity :int = 1,
                 owners :list = []
                ):
        """
        
        """

        self.I = i
        self.J = j
        self.Reservations = 0
        self.Capacity = capacity
        self.Owners = []

# class for modeling path segments
# TODO implement into other classes and modules; currently not used at all
class Segment:
    """
    
    """

    Edges        :list # 1D list of edges in segment
    Reservations :int
    Capacity     :int

    def __init__(self, 
                 edges: list,
                 capacity: int = 1
                ):
        """
        
        """

        self.Edges = edges
        self.Reservations = 0
        self.Capacity = capacity

# class for modeling warehouse grid
class Layout:
    """
    
    """

    X         :int   # number of nodes in x direction of grid (# of columns)
    Y         :int   # number of nodes in y direction of grid (# of rows)
    Nodes     :dict  # dictionary with nodes;
    Edges     :dict  # dictionary with edges; dictionary acts as adjacency matrix

    def __init__(self, 
                 x: int,
                 y: int,
                 nodecapacity: int = 1,
                 edgecapacity: int = 1
                 ):
        """
        
        """

        self.X = x
        self.Y = y

        self.Nodes = {}
        self.Edges = {}

        # SETUP NODES DICTIONARY
        for i in range(x):

            for j in range(y):

                self.Nodes[(i)*y+(j+1)] = Node(id = (i)*y+(j+1), capacity = nodecapacity)
        
        # SETUP EDGES
        for i in range(1, x+1):

            for j in range(1, y+1):

                if i == 1:      # FIRST COLUMN

                    if j == 1:  # FIRST ROW

                        if y > 1: 
                            
                            self.Edges[(1,2)] = Edge(self.Nodes[1], self.Nodes[2], capacity = edgecapacity)
                        
                        if x > 1: 
                            
                            self.Edges[(1, y+1)] = Edge(self.Nodes[1], self.Nodes[y+1], capacity = edgecapacity)

                    elif j == y: # LAST ROW
                        
                        self.Edges[(j, j-1)] = Edge(self.Nodes[j], self.Nodes[j-1], capacity = edgecapacity)

                        if x > 1:

                            self.Edges[(j, 2*j)] = Edge(self.Nodes[j], self.Nodes[2*j], capacity = edgecapacity)

                    else:
                        
                        self.Edges[(j, j-1)] = Edge(self.Nodes[j], self.Nodes[j-1], capacity = edgecapacity)
                        self.Edges[(j, j+1)] = Edge(self.Nodes[j], self.Nodes[j+1], capacity = edgecapacity)

                        self.Edges[(j, j+y)] = Edge(self.Nodes[j], self.Nodes[j+y], capacity = edgecapacity)
                
                elif i == x:      # LAST COLUMN
                
                    if j == 1:    # FIRST ROW
                        
                        self.Edges[((x-1)*y + 1, (x-2)*y+1)] = Edge(self.Nodes[(x-1)*y+1], self.Nodes[(x-2)*y+1], capacity = edgecapacity)
                        self.Edges[((x-1)*y + 1, (x-1)*y+2)] = Edge(self.Nodes[(x-1)*y+1], self.Nodes[(x-1)*y+2], capacity = edgecapacity)
                    
                    elif j == y:  # LAST

                        self.Edges[(x*y, x*y-1)] = Edge(self.Nodes[x*y], self.Nodes[x*y-1], capacity = edgecapacity)
                        self.Edges[(x*y, (x-1)*y)] = Edge(self.Nodes[x*y], self.Nodes[(x-1)*y], capacity = edgecapacity)

                    else:

                        self.Edges[((x-1)*y+j, (x-1)*y+j+1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j+1], capacity = edgecapacity)
                        self.Edges[((x-1)*y+j, (x-1)*y+j-1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j-1], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x-2)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-2)*y+j], capacity = edgecapacity)

                else:

                    if j == 1:   # FIRST ROW
                        
                        self.Edges[((x-1)*y+j, (x-1)*y+j+1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j+1], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x-2)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-2)*y+j], capacity = edgecapacity)
                        
                        self.Edges[((x-1)*y+j, (x)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x)*y+j], capacity = edgecapacity)

                    
                    elif j == y:  # LAST ROW
                    
                        self.Edges[((x-1)*y+j, (x-1)*y+j-1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j-1], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x-2)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-2)*y+j], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x)*y+j], capacity = edgecapacity)


                    else:

                        self.Edges[((x-1)*y+j, (x-1)*y+j-1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j-1], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x-1)*y+j+1)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-1)*y+j+1], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x-2)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x-2)*y+j], capacity = edgecapacity)

                        self.Edges[((x-1)*y+j, (x)*y+j)] = Edge(self.Nodes[(x-1)*y+j], self.Nodes[(x)*y+j], capacity = edgecapacity)
    
    def get_cell(self,
                 row :int,
                 col :int
                ) -> Node:
        """gets cells in specified row and column
        
        helper function that returns Node based on grid-based logic instead of continous indexing

        Args:
            row (int): row index of requested node
            col (int): column index pf requested node
        
        Returns:
            cell node (Node): returns node in specified cell

        """

        return self.Nodes[(col-1)*self.Y+row]

# class for modeling vehicles
class Vehicle:
    """
    
    """

    ID               :int     # vehicle ID
    Path_edges       :list    # 1D list of one directional edges in trajectory order
    Path_edgetimes   :list    # 1D list of movement durations per edge, with second dimensions grouping into segments in accordance with path_nodes attribute
    Loc              :any     # reference to the current location, can be Edge or Node
    Time             :int     # remaining "dwell time" on current edge # TODO NOT USED AT THE MOMENT!
    Type             :str     # specifies vehicle type (tasks may only be executed by appropriate vehicle type
    Job              :any     # job assigned to vehicle

    def __init__(self,
                 id: int,
                 type: str
                ):
        """
        
        """

        self.ID = id
        self.Path_edges = []
        self.Path_edgetimes = []
        self.Loc = None
        self.Time = 0 # TODO note: not used at the moment!
        self.Type = type
        self.Job = None # must be assigned when task is mapped to vehicle
    
    def assign_task(self,
                    edgetimes :list,       # list of ints, with dwell times per edge inferred from node sequence ("nodes" parameter)
                    nodetimes :list = []   # list of ints, with dwell times per node in the "nodes" list
                ) -> None:
        """
        
        """

        # TODO implement if decentralized task executed desired; otherwise controlled in model.py module
        # - obtain node references based on index list path_nodes
        # - obtain edge references based on index list path_nodes
        # - create segment instances
        # - assign instances  / values derived above to relevant Vehicle attributes
        pass
    
    def step(self) -> list: 
        """method facilitates one iteration of the agent-based simulation framework

        incorporates logic of vehicle moving ahead on its path

        Args:
            None

        Returns:
            outcome (list): [jobcomplete (bool), srcnodeidx (int), snknodeindex (int)] 
        
        """

        # TODO implement if decentralized movement control is desired; otherwise control vehicle movement in model.py module
        # - is path currently specified? if no, dont do anything
        # - is the next edgetime in self.Path_edgetimes still > 0? if no pop edge and arrive at node
        # - is the next segment available? OR is the next edge available
        pass

# class for modelling tasks and jobs
class Task:
    """
    
    """

    Startdate      :int
    Duedate        :int
    Type           :str       # vehicle type that is allowed
    Edges          :list
    Speeds         :list      # all edges have the same length
    Nodes_history  :list      # nodes that have already be travelled 
    Nodes_future   :list      # nodes yet to travel to
    Transporter    :Vehicle   # vehicle currently executing tasks
    Crosspoints    :list      # relevant crosspoints that this job runs through
    CPChecked      :bool      # used to indicate that this job has already been considered for cosspoint list
    Priority       :int       # optional attribute for specifying task (i.e. job) priority

    def __init__(self,
                 startdate :int,
                 enddate :int,
                 type :str,
                 edges :list,
                 speeds :list,
                 priority :int = -1 # optional constructor arg
                ):
        """
        
        """

        self.Startdate = startdate
        self.Enddate = enddate
        self.Type = type
        self.Edges = edges
        self.Speeds = speeds
        self.Nodes_history = []                                      # updated as result of vehicle movement
        self.Nodes_future = [e.I for e in edges]                     # updated as result of vehicle movement
        if len(edges)>0: self.Nodes_future.append(self.edges[-1].J)  # updated as result of vehicle movement
        self.Transporter = None
        self.Crosspoints = []
        self.Priority = priority

# class for modeling crosspoints
class Crosspoint:
    """
    
    """

    Nodeobj :Node  # node representing the crosspoint 
    Jobs    :list  # contains list of all tasks that are running via this cross point

    def __init__(self,
                 node: Node,
                 jobs: list
                ):
        """
        
        """

        self.Nodeobj = node
        self.Jobs = jobs