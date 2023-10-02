from collections import namedtuple
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NFA, State
from scipy.sparse import block_diag, dok_matrix, kron, vstack
from typing import Dict


SparseMatrix = namedtuple(
    "SparseMatrix",
    [
        "numerated_states",
        "inversed_numerated_states",
        "start_states",
        "final_states",
        "matrix",
    ],
)


def nfa_to_sparse_matrix(nfa: NFA) -> SparseMatrix:
    numerated_states = dict()
    inversed_numerated_states = dict()
    i = 0
    for state in nfa.states:
        numerated_states[state] = i
        inversed_numerated_states[i] = state
        i += 1

    nfa_dict = nfa.to_dict()
    matrix = dict()

    for symbol in nfa.symbols:
        curr_symbol_matrix = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
        for state_from, transitions in nfa_dict.items():
            # States that can be reached from the state_from in one step.
            states_to = set()
            if symbol in transitions:
                states_to = transitions[symbol]
            if type(states_to) is State:
                states_to = {states_to}

            for state_to in states_to:
                curr_symbol_matrix[
                    numerated_states[state_from], numerated_states[state_to]
                ] = True

        matrix[symbol] = curr_symbol_matrix

    return SparseMatrix(
        numerated_states,
        inversed_numerated_states,
        nfa.start_states,
        nfa.final_states,
        matrix,
    )


def sparse_matrix_to_nfa(sparse_matrix: SparseMatrix) -> NFA:
    nfa = NFA()

    for symbol in sparse_matrix.matrix.keys():
        for key in sparse_matrix.matrix[symbol].keys():
            state_from, state_to = key
            nfa.add_transition(
                sparse_matrix.inversed_numerated_states[state_from],
                symbol,
                sparse_matrix.inversed_numerated_states[state_to],
            )

    for start_state in sparse_matrix.start_states:
        nfa.add_start_state(start_state)
    for final_state in sparse_matrix.final_states:
        nfa.add_final_state(final_state)

    return nfa


def intersect(
    sparse_matrix1: SparseMatrix, sparse_matrix2: SparseMatrix
) -> SparseMatrix:
    symbols = sparse_matrix1.matrix.keys() & sparse_matrix2.matrix.keys()

    numerated_states = {}
    start_states = set()
    final_states = set()
    matrix = dict()

    for state1, state1_number in sparse_matrix1.numerated_states.items():
        for state2, state2_number in sparse_matrix2.numerated_states.items():
            state = len(sparse_matrix2.numerated_states) * state1_number + state2_number
            numerated_states[state] = state

            if (
                state1 in sparse_matrix1.start_states
                and state2 in sparse_matrix2.start_states
            ):
                start_states.add(state)

            if (
                state1 in sparse_matrix1.final_states
                and state2 in sparse_matrix2.final_states
            ):
                final_states.add(state)

    for symbol in symbols:
        matrix[symbol] = kron(
            sparse_matrix1.matrix[symbol], sparse_matrix2.matrix[symbol], format="dok"
        )

    inversed_numerated_states = numerated_states

    return SparseMatrix(
        numerated_states, inversed_numerated_states, start_states, final_states, matrix
    )


def create_front(
    graph_smatrix: SparseMatrix,
    regex_smatrix: SparseMatrix,
    numerated_start_states: Dict,
) -> dok_matrix:
    front_row = dok_matrix((1, len(graph_smatrix.numerated_states)), dtype=bool)
    front = dok_matrix(
        (
            len(regex_smatrix.numerated_states),
            len(graph_smatrix.numerated_states) + len(regex_smatrix.numerated_states),
        ),
        dtype=bool,
    )
    for i in numerated_start_states:
        front_row[0, i] = True
    for i in regex_smatrix.start_states:
        front[
            regex_smatrix.numerated_states[i], regex_smatrix.numerated_states[i]
        ] = True
        front[
            regex_smatrix.numerated_states[i], len(regex_smatrix.numerated_states) :
        ] = front_row
    return front


def upd_front(regex_smatrix: SparseMatrix, front: dok_matrix) -> dok_matrix:
    upd_front = dok_matrix(front.shape, dtype=bool)
    states_count = len(regex_smatrix.numerated_states)
    for i, j in zip(*front.nonzero()):
        if j < states_count:
            if front[i, states_count:].count_nonzero() > 0:
                upd_front[(i // states_count * states_count) + j, j] = True
                upd_front[
                    (i // states_count * states_count) + j, states_count:
                ] += front[i, states_count:]
    return upd_front


def bfs(
    graph_smatrix: SparseMatrix,
    regex_smatrix: SparseMatrix,
    foreach_start_node: bool = False,
) -> set:
    if not graph_smatrix.start_states:
        return set()
    numerated_start_states = [
        graph_smatrix.numerated_states[s] for s in graph_smatrix.start_states
    ]
    if foreach_start_node:
        front = vstack(
            [
                create_front(graph_smatrix, regex_smatrix, {i})
                for i in numerated_start_states
            ]
        )
    else:
        front = create_front(graph_smatrix, regex_smatrix, numerated_start_states)

    direct_sum = dict()
    labels = set(graph_smatrix.matrix.keys()).intersection(
        set(regex_smatrix.matrix.keys())
    )
    for label in labels:
        direct_sum[label] = dok_matrix(
            block_diag((regex_smatrix.matrix[label], graph_smatrix.matrix[label]))
        )

    attended = dok_matrix(front.shape, dtype=bool)
    while True:
        saved_attended = attended.copy()
        for ds_matrix in direct_sum.values():
            next_front = attended @ ds_matrix if front is None else front @ ds_matrix
            attended += upd_front(regex_smatrix, next_front)
        if saved_attended.count_nonzero() == attended.count_nonzero():
            break
        front = None

    ans = set()
    graph_states_keys = list(graph_smatrix.numerated_states.keys())
    regex_states_keys = list(regex_smatrix.numerated_states.keys())
    regex_states_count = len(regex_smatrix.numerated_states)
    for i, j in zip(*attended.nonzero()):
        if (
            regex_states_keys[i % regex_states_count] in regex_smatrix.final_states
            and regex_states_count <= j
        ):
            if graph_states_keys[j - regex_states_count] in graph_smatrix.final_states:
                if foreach_start_node:
                    ans.add(
                        (
                            numerated_start_states[i // regex_states_count],
                            j - regex_states_count,
                        )
                    )
                else:
                    ans.add(j - regex_states_count)
    return ans
