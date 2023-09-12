from typing import Tuple
import networkx as nx
from cfpq_data import *


class GraphData:
    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self.number_of_nodes = graph.number_of_nodes()
        self.number_of_edges = graph.number_of_edges()
        self.labels = set(get_sorted_labels(graph))
        return


def get_graph_info(graph_name: str) -> GraphData:
    return GraphData(graph_from_csv(download(graph_name)))


def get_labeled_two_cycles_graph(
        first_cycle_nodes_num: int, second_cycle_nodes_num: int, labels: Tuple[str, str]) -> nx.MultiDiGraph:
    return labeled_two_cycles_graph(first_cycle_nodes_num, second_cycle_nodes_num, labels=labels)


def save_graph_dot(graph: nx.MultiDiGraph, path: str) -> None:
    nx.drawing.nx_pydot.write_dot(graph, path)
