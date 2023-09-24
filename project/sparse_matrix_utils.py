from collections import namedtuple
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NFA, State
from scipy.sparse import dok_matrix, kron

SparseMatrix = namedtuple(
    "SparseMatrix", [ "numerated_states", "inversed_numerated_states", "start_states", "final_states", "matrix" ]
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
                curr_symbol_matrix[ numerated_states[state_from], numerated_states[state_to] ] = True

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


def intersect(sparse_matrix1: SparseMatrix, sparse_matrix2: SparseMatrix) -> SparseMatrix:
    symbols = sparse_matrix1.matrix.keys() & sparse_matrix2.matrix.keys()

    numerated_states = {}
    start_states = set()
    final_states = set()
    matrix = dict()

    for state1, state1_number in sparse_matrix1.numerated_states.items():
        for state2, state2_number in sparse_matrix2.numerated_states.items():
            state = len(sparse_matrix2.numerated_states) * state1_number + state2_number
            numerated_states[state] = state

            if state1 in sparse_matrix1.start_states and state2 in sparse_matrix2.start_states:
                start_states.add(state)

            if state1 in sparse_matrix1.final_states and state2 in sparse_matrix2.final_states:
                final_states.add(state)

    for symbol in symbols:
        matrix[symbol] = kron(sparse_matrix1.matrix[symbol], sparse_matrix2.matrix[symbol], format="dok")
    
    inversed_numerated_states = numerated_states

    return SparseMatrix(numerated_states, inversed_numerated_states, start_states, final_states, matrix)
