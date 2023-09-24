import project.automaton_utils as automaton_utils
import project.sparse_matrix_utils as sparse_matrix_utils
from pyformlang.finite_automaton import DeterministicFiniteAutomaton as DFA, State
from pyformlang.regular_expression import Regex


def test_intersect() -> None:
    state0 = State(555)
    state1 = State(5555)
    state2 = State(55555)
    automaton = DFA()
    automaton.add_start_state(state0)
    automaton.add_final_state(state1)
    automaton.add_transitions(
            [(state0, "b", state0), (state0, "a", state1), (state1, "b", state1), (state1, "a", state2), (state2, "b", state2), (state2, "a", state2)]
        
        )
    #           Automaton #1.
    #       _           _             _
    #     b| ↓  a     b| ↓    a   a,b| ↓ 
    # -> (555) ---> ((5555)) ---> (55555)

    stateq0 = State(111)
    stateq1 = State(1111)
    stateq2 = State(11111)
    automaton1 = DFA()
    automaton1.add_start_state(stateq0)
    automaton1.add_final_state(stateq1)
    automaton1.add_transitions(
            [(stateq0, "a", stateq0), (stateq0, "b", stateq1), (stateq1, "a", stateq1), (stateq1, "b", stateq2), (stateq2, "b", stateq2), (stateq2, "a", stateq2)]
        
        )
    #           Automaton #2.
    #       _           _             _
    #     a| ↓  b     a| ↓    b   a,b| ↓ 
    # -> (111) ---> ((1111)) ---> (11111)

    automaton_trans = sparse_matrix_utils.sparse_matrix_to_nfa(sparse_matrix_utils.intersect(sparse_matrix_utils.nfa_to_sparse_matrix(automaton), sparse_matrix_utils.nfa_to_sparse_matrix(automaton1)))

    expected_automaton = DFA()
    states = [State(i) for i in range(0,9)]
    expected_automaton.add_start_state(states[0])
    expected_automaton.add_final_state(states[4])
    expected_automaton.add_transitions([
         (states[0], "b", states[1]), (states[0], "a", states[3]), (states[1], "a", states[4]),
         (states[1], "b", states[2]), (states[2], "b", states[2]), (states[2], "a", states[5]),
         (states[3], "a", states[6]), (states[3], "b", states[4]), (states[4], "a", states[7]),
         (states[4], "b", states[5]), (states[5], "a", states[8]), (states[5], "b", states[5]),
         (states[6], "a", states[6]), (states[6], "b", states[7]), (states[7], "a", states[7]),
         (states[7], "b", states[8]), (states[8], "a", states[8]), (states[8], "b", states[8])
    ])
    #      Expected Automaton.
    #           a        a    |‾↓a
    #   -> (0) ---> (3) --->  (6) 
    #      b↓   a    b↓    a   b↓  ˱_
    #      (1) ---> ((4)) ---> (7)  _|a
    #      b↓   a    b↓   a     b↓ 
    #      (2) ---> (5) --->   (8)
    #     b↑_|      b↑_|    a,b↑_|

    assert expected_automaton.is_equivalent_to(automaton_trans)


def test_nfa_to_sparse_matrix_and_back() -> None:
    r = Regex("(a+b+$)*c")
    expected_dfa = automaton_utils.regex_to_min_dfa(r)
    dfa = sparse_matrix_utils.sparse_matrix_to_nfa(sparse_matrix_utils.nfa_to_sparse_matrix(expected_dfa))
   
    assert dfa.is_equivalent_to(expected_dfa)

def test_intersect_with_empty_automaton() -> None:
    state0 = State(1)
    state1 = State(2)
    state2 = State(3)
    automaton = DFA()
    automaton.add_start_state(state0)
    automaton.add_final_state(state1)
    automaton.add_transitions(
            [(state0, "b", state0), (state0, "a", state1), (state1, "b", state1), (state1, "a", state2), (state2, "b", state2), (state2, "a", state2)]
        
        )
    
    automaton1 = DFA()

    automaton_trans = sparse_matrix_utils.sparse_matrix_to_nfa(sparse_matrix_utils.intersect(sparse_matrix_utils.nfa_to_sparse_matrix(automaton), sparse_matrix_utils.nfa_to_sparse_matrix(automaton1)))

    assert automaton1.is_equivalent_to(automaton_trans)

def test_intersect_with_empty_automaten() -> None:
    automaton = DFA()
    automaton1 = DFA()
    automaton_trans = sparse_matrix_utils.sparse_matrix_to_nfa(sparse_matrix_utils.intersect(sparse_matrix_utils.nfa_to_sparse_matrix(automaton), sparse_matrix_utils.nfa_to_sparse_matrix(automaton1)))

    assert automaton.is_equivalent_to(automaton_trans)
    assert automaton1.is_equivalent_to(automaton_trans)

def test_intersect_with_one_state_automaton() -> None:
    state0 = State(1)
    state1 = State(2)
    state2 = State(3)
    automaton = DFA()
    automaton.add_start_state(state0)
    automaton.add_final_state(state1)
    automaton.add_transitions(
            [(state0, "b", state0), (state0, "a", state1), (state1, "b", state1), (state1, "a", state2), (state2, "b", state2), (state2, "a", state2)]
        
        )
    
    automaton1 = DFA()
    automaton1.add_start_state(State(5))
    automaton1.add_final_state(State(5))

    empty_automaton = DFA()

    automaton_trans = sparse_matrix_utils.sparse_matrix_to_nfa(sparse_matrix_utils.intersect(sparse_matrix_utils.nfa_to_sparse_matrix(automaton), sparse_matrix_utils.nfa_to_sparse_matrix(automaton1)))

    assert empty_automaton.is_equivalent_to(automaton_trans)
