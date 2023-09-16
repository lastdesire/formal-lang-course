from typing import Set

from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    EpsilonNFA as ENFA,
    DeterministicFiniteAutomaton as DFA,
    NondeterministicFiniteAutomaton as NFA,
)
from pyformlang.regular_expression import Regex
from typing import Union


def regex_to_min_dfa(r: Regex) -> DFA:
    return r.to_epsilon_nfa().to_deterministic().minimize()


def graph_to_enfa(
    graph: MultiDiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    is_epsilon_forbidden: bool = False,
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
