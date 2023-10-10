from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    EpsilonNFA as ENFA,
    DeterministicFiniteAutomaton as DFA,
    NondeterministicFiniteAutomaton as NFA,
)
from typing import Set, Union
from scipy.sparse import dok_matrix, lil_matrix, csr_matrix, csc_matrix
import project.sparse_matrix_utils as sparse_matrix_utils


def regex_to_min_dfa(r: Regex) -> DFA:
    return r.to_epsilon_nfa().minimize()


def graph_to_nfa(
    graph: MultiDiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    is_epsilon_forbidden: bool = True,
) -> Union[ENFA, NFA]:
    if is_epsilon_forbidden:
        automaton = NFA.from_networkx(graph)
    else:
        automaton = ENFA.from_networkx(graph)

    if start_nodes is None:
        for node in graph.nodes:
            automaton.add_start_state(node)
    else:
        for node in start_nodes:
            automaton.add_start_state(node)

    if final_nodes is None:
        for node in graph.nodes:
            automaton.add_final_state(node)
    else:
        for node in final_nodes:
            automaton.add_final_state(node)

    return automaton


def rpq(
    graph: MultiDiGraph,
    regex: Regex,
    start_states: set = None,
    final_states: set = None,
    matrix_type: Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix] = dok_matrix,
) -> set:
    rpq = set()
    matrix_from_graph = sparse_matrix_utils.nfa_to_sparse_matrix(
        graph_to_nfa(graph, start_states, final_states), matrix_type
    )
    matrix_from_regex = sparse_matrix_utils.nfa_to_sparse_matrix(
        regex_to_min_dfa(regex), matrix_type
    )
    matrix_from_regex_states_count = len(matrix_from_regex.numerated_states)
    intersection_matrix = sparse_matrix_utils.intersect(
        matrix_from_graph, matrix_from_regex, matrix_type
    )

    if not intersection_matrix.matrix.values():
        matrix = matrix_type((1, 1))
    else:
        matrix = sum(intersection_matrix.matrix.values())
        prev_nonzeros = matrix.count_nonzero()
        curr_nonzeros = 0

        while prev_nonzeros != curr_nonzeros:
            matrix += matrix @ matrix
            prev_nonzeros = curr_nonzeros
            curr_nonzeros = matrix.count_nonzero()

    for state_from, state_to in zip(*matrix.nonzero()):
        if (
            state_from in intersection_matrix.start_states
            and state_to in intersection_matrix.final_states
        ):
            rpq.add(
                (
                    state_from // matrix_from_regex_states_count,
                    state_to // matrix_from_regex_states_count,
                )
            )

    rpq_result = set()
    for state1, state2 in rpq:
        rpq_result.add(
            (
                matrix_from_graph.inversed_numerated_states[state1],
                matrix_from_graph.inversed_numerated_states[state2],
            )
        )

    return rpq_result


def bfs_rpq(
    graph: MultiDiGraph,
    regex: Regex,
    start_states: set = None,
    final_states: set = None,
    foreach_start_node: bool = False,
    matrix_type: Union[lil_matrix, dok_matrix, csr_matrix, csc_matrix] = dok_matrix
) -> set:
    if (
        regex_to_min_dfa(regex).is_empty()
        or {}
        == sparse_matrix_utils.nfa_to_sparse_matrix(regex_to_min_dfa(regex), matrix_type).matrix
    ):
        if start_states:
            return start_states
        return graph.nodes
    return sparse_matrix_utils.bfs(
        sparse_matrix_utils.nfa_to_sparse_matrix(
            graph_to_nfa(graph, start_states, final_states), matrix_type
        ),
        sparse_matrix_utils.nfa_to_sparse_matrix(regex_to_min_dfa(regex), matrix_type),
        foreach_start_node, matrix_type
    )
