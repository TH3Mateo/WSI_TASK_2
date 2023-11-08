import matplotlib.pyplot as plt
import networkx as nx


def matrix_print(matrix):
    # helper function to print matrixes
    print("*****************************************")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print("*****************************************")


def show_seed(seed):
    plt.imshow(seed)
    plt.show()


def show_field(v_matrix):
    # function to show the generated/loaded graph before the algorithm starts

    graph = nx.Graph()
    for i in range(len(v_matrix)):
        graph.add_node(i)

    for i in range(len(v_matrix)):
        for j in range(len(v_matrix[i])):

            if v_matrix[i][j] == 1:
                graph.add_edge(i, j, weight=1, color="black")

    weights = nx.get_edge_attributes(graph, 'weight').values()
    colors = nx.get_edge_attributes(graph, 'color').values()
    labels = dict(zip(graph.nodes(), range(len(v_matrix))))
    pos = nx.get_node_attributes(graph, 'pos').values()
    # pos = nx.spring_layout(graph)
    nx.draw(graph, pos=nx.shell_layout(graph), labels=labels, edge_color=colors, width=list(weights), with_labels=True)
    plt.show()
    # print(list(graph.nodes(data="pos")))
    print(nx.get_node_attributes(graph, 'pos'))

    return graph.copy()


def show_update(graph, lit_v, vertexes, nodes):
    # loads base graph and updates it, including algorithm's results
    # green node - turned on, blue - turned off
    # green vertex - covered, red - uncovered

    updated = graph.copy()

    colormap = []
    for i in range(len(nodes)):
        if nodes[i] == 1:
            colormap.append("green")
        else:
            colormap.append("blue")

    for i in range(len(lit_v)):
        for j in range(len(lit_v[i])):
            if lit_v[i][j] and vertexes[i][j]:
                updated.remove_edge(i, j)
                updated.add_edge(i, j, color="green", width=2)

            elif lit_v[i][j] == 0 and vertexes[i][j]:
                updated.remove_edge(i, j)
                updated.add_edge(i, j, color="red", width=1)

    colors = nx.get_edge_attributes(updated, 'color').values()
    weights = nx.get_edge_attributes(updated, 'weight').values()
    nx.draw(updated, pos=nx.shell_layout(updated), node_color=colormap, edge_color=colors, width=list(weights),
            labels=dict(zip(updated.nodes(), range(len(updated)))), with_labels=True)
    plt.show()
