from typing import Tuple
import networkx as nx
import cfpq_data as cd


class GraphData:
    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self.number_of_nodes = graph.number_of_nodes()
        self.number_of_edges = graph.number_of_edges()
        self.labels = set(cd.get_sorted_labels(graph))
        self.sorted_labels_list = cd.get_sorted_labels(graph)
        return


def get_graph_info(graph_name: str) -> GraphData:
    return GraphData(cd.graph_from_csv(cd.download(graph_name)))


def get_labeled_two_cycles_graph(
    first_cycle_nodes_num: int, second_cycle_nodes_num: int, labels: Tuple[str, str]
) -> nx.MultiDiGraph:
    return cd.labeled_two_cycles_graph(
        first_cycle_nodes_num, second_cycle_nodes_num, labels=labels
    )


def save_graph_dot(graph: nx.MultiDiGraph, path: str) -> None:
    nx.drawing.nx_pydot.write_dot(graph, path)


def read_graph_dot(path: str) -> nx.MultiDiGraph:
    graph = nx.drawing.nx_pydot.read_dot(path)
    if "\n" in graph.nodes:
        graph.remove_node("\n")
    if "\\n" in graph.nodes:
        graph.remove_node("\\n")
    return graph
