def print_DAG(DAG_model):
    # create a dict to visualize the dependendies
    print('  - NODES:')
    print(DAG_model.nodes())
    depend_dict = {}
    for connection in DAG_model.edges():
        
        if not connection[0] in depend_dict.keys():
            depend_dict[connection[0]] = [connection[1]]
        else:
            depend_dict[connection[0]].append(connection[1])

    nodes_in_DAG = set()
    for edge in DAG_model.edges():
        nodes_in_DAG.add(edge[0])
        nodes_in_DAG.add(edge[1])

    print('  - EDGES:')
    # nodes_in_DAG imposes an ordering of variables for the plot
    for feature in nodes_in_DAG:
        for key in depend_dict.keys():
            if key == feature:
                print(str(key)+" -> "+str(depend_dict[key]))


def extract_subset_CPDs(original_cpds, variables_subset):
    # Initialize an empty list to store the subset of CPDs
    subset_cpds = []

    # Iterate over all CPDs
    for cpd in original_cpds:
        if cpd.variable in variables_subset:
            subset_cpds.append(cpd)

    return subset_cpds

