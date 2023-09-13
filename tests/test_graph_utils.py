import os
import project.graph_utils as utils
import cfpq_data as cd
from filecmp import cmp


def test_get_graph_info() -> None:
    graph_info = utils.get_graph_info("travel")
    assert 277 == graph_info.number_of_edges
    assert 131 == graph_info.number_of_nodes
    assert {
        "range",
        "domain",
        "complementOf",
        "equivalentClass",
        "inverseOf",
        "comment",
        "minCardinality",
        "type",
        "versionInfo",
        "rest",
        "oneOf",
        "hasPart",
        "someValuesFrom",
        "hasAccommodation",
        "differentFrom",
        "subClassOf",
        "disjointWith",
        "first",
        "unionOf",
        "hasValue",
        "intersectionOf",
        "onProperty",
    } == graph_info.labels


def test_get_labeled_two_cycles_graph() -> None:
    graph = utils.get_labeled_two_cycles_graph(5, 5, labels=("x", "y"))
    assert 12 == graph.number_of_edges()
    assert 11 == graph.number_of_nodes()
    assert {"x", "y"} == set(cd.get_sorted_labels(graph))


def test_save_graph_dot() -> None:
    # There is the path to expected graph from upper test.
    expected_graph_path = os.curdir + "/output/task_1/some_graph.dot"
    graph_path = os.curdir + "/output/task_1/some_other_graph.dot"
    graph = cd.labeled_two_cycles_graph(5, 5, labels=("x", "y"))
    utils.save_graph_dot(graph, graph_path)
    try:
        assert cmp(expected_graph_path, graph_path, shallow=False)
    finally:
        os.remove(graph_path)
