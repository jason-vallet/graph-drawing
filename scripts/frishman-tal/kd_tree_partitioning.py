from tulip import tlp
from collections import deque
import math
import random

PARTITION_SIZE = 100

## \brief Computes the partitions of the graph
# \param graph The graph to partition
# \param max_partition_size The maximum size of a partition
# \return A list of list of tlp.node corresponding to each partition
def run(graph, max_partition_size):
    if graph.numberOfNodes() <= max_partition_size: return [graph.nodes()]
     
    layout = graph.getLayoutProperty("viewLayout")
    quit = False
    count = 0
    partitions = deque()
    partitions.append(graph.nodes())
    while not quit:
        nb_partitions = len(partitions)
        for i in range(nb_partitions):
            p = partitions.popleft()
            p_size = len(p)

            # sort the partition by x and y coord alternatively
            p.sort(key = lambda pos: layout[pos].x()) if count % 2 == 0 else p.sort(key = lambda pos: layout[pos].y())

            # cut the partition in two and push the 2 new partitions in the queue
            median_index = p_size // 2
            partitions.append(p[median_index:])
            partitions.append(p[:median_index])     
            
            # terminate when we have reached the ideal partition size             
            quit = (p_size // 2 if p_size % 2 == 0 else (p_size // 2) + 1) <= max_partition_size            
        count += 1
    return partitions


# def run(graph, max_partition_size):    
#     if graph.numberOfNodes() <= max_partition_size: return 
    
#     layout = graph.getLayoutProperty("viewLayout")
#     graph.addCloneSubGraph("partition_0")
    
#     quit = False
#     count = 0
#     p_count = 1

#     while not quit:
#         for p in graph.getSubGraphs():
#             if p.getName().startswith("partition"):
#                 p_size = p.numberOfNodes()
#                 p_nodes = p.nodes() # we use a list of nodes because there's no way to efficiently create a sub-graph via an IteratorNode
                
#                 # sort the partition by x and y coord alternatively
#                 p_nodes.sort(key = lambda pos: layout[pos].x()) if count % 2 == 0 else p_nodes.sort(key = lambda pos: layout[pos].y()) 

#                 # cut the partition in two, create their induced sub-graph and delete the current partition 
#                 median_index = p_size // 2
#                 graph.inducedSubGraph(p_nodes[median_index:], None, "partition_{}".format(p_count))
#                 graph.inducedSubGraph(p_nodes[:median_index], None, "partition_{}".format(p_count + 1))            
#                 graph.delSubGraph(p)
                
#                 # terminate when we have reached the ideal partition size 
#                 if (p_size // 2 if p_size % 2 == 0 else (p_size // 2) + 1) <= max_partition_size: quit = True
#                 p_count += 2         
#         count += 1

## \brief Deletes every partition of the graph
# \param graph The graph on which we delete all partitions
def delete_partitions(graph):
    for sub in graph.getSubGraphs():
        if sub.getName().startswith("partition"):
            graph.delSubGraph(sub)

## \brief Creates partition sub-graphs from a list of list of nodes
# \param graph The graph which will receive the partition sub-graphs
# \param partitions A list of list of tlp.node corresponding to each partition
def create_subgraphs(graph, partitions):
    count = 0
    for p in partitions:
        graph.inducedSubGraph(p, None, "partition_{}".format(count))
        count += 1

## \brief Returns a list of the graph partitions (sub-graph)
# \return Returns a list of list of tlp.node corresponding to each partition
def get_partitions(graph):
    partitions = [p for p in graph.getSubGraphs() if p.getName().startswith("partition")]
    return partitions if len(partitions) > 0 else [graph]

## \brief Colors the nodes according to the partition they belong in, and prints the size of the largest partition found.
# \param graph The graph containing the partitions
# \param partitions A list of list of tlp.node corresponding to each partition
def debug(graph, partitions):
    colors = graph.getColorProperty("viewColor")
    max_size = 0
    for p in partitions:
        p_size = len(p)
        if p_size > max_size: max_size = p_size
        r = random.randrange(255)
        g = random.randrange(255)
        b = random.randrange(255)
        for n in p:
            colors[n] = tlp.Color(r, g, b)
    print("max partition size found : {}".format(max_size))

def main(graph):
    partitions = run(graph, PARTITION_SIZE)
    debug(graph, partitions)
    
    
    