def add_next_nodes(node_neighbours,next_nodes):
    """Adds the node neighbours to the next nodes list only if the neighbour is not already on the list
        Parameters
        ----------
        node_neighbours: list
            The neigbours of the node
        next_nodes:list
            The nodes that are going to be visited 
        Returns
        -------
        next_nodes:list
            The next_nodes list with the node neighbours that werent already on the list
         """
    for node_neighbour in node_neighbours:
        if node_neighbour in next_nodes:
            pass
        next_nodes.append(node_neighbour)
    return next_nodes


def bfs(graph,root_node):
    """ Travels the recived graph wiht the Breadth-First-Search algorithim
        Parameters
        ----------
        graph: list
            The graph to go through 
        root_node: integer
            The node that will start the bfs
        Returns
        -------
        visited_nodes: list
            The list with the visited nodes in the order they were visited
    """
    if [] in graph:
        raise Exception("bfs doesnt work in disconnected graphs")        
    visited_nodes = [root_node] #The root node will be the first visited node
    next_nodes = [] #We are going to use this list as a  queue to travel the nodes in the bfs way
    try:
        add_next_nodes(graph[root_node],next_nodes)
    except IndexError as ie:
        raise Exception(("There isn´t a node {} in this graph").format(root_node))
    while(next_nodes):
        actual_node = next_nodes.pop(0)
        if actual_node in visited_nodes:
            pass
        else:
            visited_nodes.append(actual_node)
            add_next_nodes(graph[actual_node],next_nodes)
    return visited_nodes    

if __name__ == "__main__":
    print(bfs([[1,2,3],[0,3],[0,3],[0,1,2,4],[3]],0)) #Example 1
    print(bfs([[1,2],[0,3,4],[0,5,6],[1],[1],[2],[2]],6)) #Example 2
    print(bfs([[1,4],[0,2,3],[1],[1,4],[3,0]],4)) #Example 3