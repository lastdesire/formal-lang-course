import os
import cfpq_data as cd
import project.automaton_utils as utils
import project.graph_utils as graph_utils
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton as DFA, State


def test_regex_to_min_dfa_1():
    r = Regex("a+b+c")
    dfa = utils.regex_to_min_dfa(r)

    assert dfa.is_deterministic()
    assert dfa.accepts("a")
    assert dfa.accepts("b")
    assert dfa.accepts("c")
    assert not dfa.accepts("d")
    assert not dfa.accepts("ab")
    assert not dfa.accepts("cc")
    assert not dfa.accepts("abc")
    assert not dfa.accepts("")

    state0 = State(0)
    state1 = State(1)
    expected_dfa = DFA()
    expected_dfa.add_start_state(state0)
    expected_dfa.add_final_state(state1)
    expected_dfa.add_transitions(
        [(state0, "a", state1), (state0, "b", state1), (state0, "c", state1)]
    )

    assert dfa.is_equivalent_to(expected_dfa)


def test_regex_to_min_dfa_2():
    r = Regex("(a+b+$)*c")
    dfa = utils.regex_to_min_dfa(r)

    assert dfa.is_deterministic
    assert dfa.accepts("ac")
    assert dfa.accepts("c")
    assert dfa.accepts("ababababac")
    assert not dfa.accepts("ca")
    assert not dfa.accepts("")

    state0 = State(0)
    state1 = State(1)
    expected_dfa = DFA()
    expected_dfa.add_start_state(state0)
    expected_dfa.add_final_state(state1)
    expected_dfa.add_transitions(
        [(state0, "a", state0), (state0, "b", state0), (state0, "c", state1)]
    )

    assert dfa.is_equivalent_to(expected_dfa)


def test_regex_to_min_dfa_3():
    r = Regex("$")
    dfa = utils.regex_to_min_dfa(r)

    assert {} == dfa.to_dict()
    assert dfa.start_states == dfa.final_states

    r_eq = Regex("$*")
    dfa_eq = utils.regex_to_min_dfa(r_eq)

    assert dfa.is_equivalent_to(dfa_eq)


def test_graph_to_nfa_1():
    graph = cd.graph_from_csv(cd.download("travel"))
    nfa = utils.graph_to_nfa(graph)
    enfa = utils.graph_to_nfa(graph, is_epsilon_forbidden=False)

    assert nfa.is_equivalent_to(enfa)
    assert 131 == len(nfa.start_states)
    assert 131 == len(nfa.final_states)
    expected_edges_count = 0
    for target_node in nfa.to_dict().values():
        for automaton_edge in target_node.values():
            expected_edges_count += len(automaton_edge)
    assert 277 == expected_edges_count


def test_graph_to_nfa_2():
    graph = cd.graph_from_csv(cd.download("atom"))
    nfa = utils.graph_to_nfa(graph, start_nodes={0, 5, 10, 15}, final_nodes={4, 10, 16})

    assert {0, 5, 10, 15} == nfa.start_states
    assert {4, 10, 16} == nfa.final_states
    expected_edges_count = 0
    for target_node in nfa.to_dict().values():
        for automaton_edge in target_node.values():
            expected_edges_count += len(automaton_edge)
    assert 425 == expected_edges_count


def test_graph_to_nfa_3():
    graph = graph_utils.get_labeled_two_cycles_graph(5, 100, labels=("x", "y"))
    nfa = utils.graph_to_nfa(graph, start_nodes={0})

    assert {0} == nfa.start_states
    assert 106 == len(nfa.final_states)
    expected_edges_count = 0
    for target_node in nfa.to_dict().values():
        for automaton_edge in target_node.values():
            expected_edges_count += len(automaton_edge)
    assert 107 == expected_edges_count


def test_graph_to_nfa_4():
    graph = graph_utils.read_graph_dot(
        os.curdir + "/tests/output/task_1/some_graph.dot"
    )
    nfa = utils.graph_to_nfa(graph)

    assert 11 == len(nfa.start_states)
    assert 11 == len(nfa.final_states)
    expected_edges_count = 0
    for target_node in nfa.to_dict().values():
        for automaton_edge in target_node.values():
            expected_edges_count += len(automaton_edge)
    assert 12 == expected_edges_count


def test_rpq() -> None:
    regex = Regex("(a+b)*b")
    #   Equiv automaton for regex (0+1)*1.
    #   |‾↓a  b    |‾↓b
    # ->(0) ---> ((1))
    #       <---
    #        a

    state0 = State(5)
    state1 = State(10)
    state2 = State(15)
    automaton1 = DFA()
    # automaton1.add_start_state(state0)
    # automaton1.add_final_state(state1)
    # automaton1.add_final_state(state2)
    automaton1.add_transitions(
        [
            (state0, "a", state0),
            (state0, "b", state1),
            (state1, "a", state0),
            (state1, "b", state1),
            (state0, "c", state2),
            (state1, "c", state2),
            (state2, "b", state2),
            (state2, "a", state2),
            (state2, "c", state2),
        ]
    )
    #   Automaton #2.
    #   |‾↓a  b    |‾↓b
    # ->(0) ---> ((1))
    #    |  <---   |
    #  c |    a    | c
    #    |___   ___|
    #       ↓   ↓
    #       ((2))

    graph = automaton1.to_networkx()
    res = utils.rpq(graph, regex, {state0}, {state1, state2})
    expected_rpq_result = {(5, 10)}
    expected_rpq_result_reversed = {(10, 5)}

    assert expected_rpq_result == res or expected_rpq_result_reversed == res
