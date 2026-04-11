def bfs(queue: list, visited: dict, get_neighbors: "func"):
    # NEW
    for root in queue:
        visited[root] = 0  # root -> col index (not just True)

    from collections import defaultdict
    col_nodes_map = defaultdict(list)
    # END NEW

    while queue:
        node = queue.popleft()
	
	# NEW
        col_nodes_map[visited[node]].append(node)

        # get_neighbors -> [(node, ±1 for left/right child), ...]
        for next_node, delta_col in get_neighbors(node):

            if (
                _is_valid(next_node)
                and next_node not in visited
            ):
                visited[next_node] = visited[node] + delta_col
	 # END NEW

                queue.append(next_node)

    return col_nodes_map