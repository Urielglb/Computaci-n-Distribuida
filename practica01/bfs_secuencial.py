def add_next_nodes(node_neighbours,next_nodes):
    for node_neighbour in node_neighbours:
        if node_neighbour in next_nodes:
            pass
        next_nodes.append(node_neighbour)
    return next_nodes


def bfs(graph):
    if(not graph):
        return
    visited_nodes = [0]
    next_nodes = []
    add_next_nodes(graph[0],next_nodes)
    if not next_nodes:
        return visited_nodes
    while(next_nodes):
        actual_node = next_nodes.pop(0)
        if actual_node in visited_nodes:
            pass
        else:
            visited_nodes.append(actual_node)
            add_next_nodes(graph[actual_node],next_nodes)
    return visited_nodes    

if __name__ == "__main__":
    print(bfs([[1,2,3],[0,3],[0,3],[0,1,2,4],[3]]))
    print(bfs([[1,2],[3,4],[5,6],[],[],[],[]]))
    print(bfs([[1,4],[0,2,3],[1],[1,4],[3,0]]))