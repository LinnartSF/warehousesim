""" 

this module contains functions that are supposed to make life easier

__author__ = "Linnart Felkl"
__email__ = "LinnartSF@gmail.com"

"""

def get_edges(nodeseq: list) -> tuple:
    """returns edge indices, derived from node sequence

    this function returns edge indices, derived from the forwarded node index sequence
    edge indices are returned as a list of tuples
    the edge index list returned can be used to access edge references in Layout instances (e.g. .Grid attribute of Model class instance in modelling.py)

    Args:
        nodeseq (list): sequence of nodes for which edges are to be derived (ints)
    
    Returns:
        edgeseq (list): list of derived edge indices (int tuples)

    """

    edges = []

    for i in range(0,len(nodeseq)-1):

        edges.append((nodeseq[i], nodeseq[i+1]))

    return edges