class FiniteAutomaton:
    def __init__(self, num_states: int | list[int], alphabet:str| list[str], final_states=[]):
        assert isinstance(alphabet, str) or isinstance(alphabet, list) and all(isinstance(c, str) for c in alphabet), "The alphabet should be either a string or a list of strings"
        assert num_states > 0, "The value of num_states cannot be less than 1"
        
        self.num_states = num_states
        self.alphabet = list(alphabet) if isinstance(alphabet, str) else alphabet
        self.transitions = {}
        self.current_state = 0
        self.final_states = final_states

    def add_final_states(self, states:list[int]):
        self.final_states.extend(states)
        
    def add_transition(self, origin_state:int, end_state:int, input_symbols:str | list[str]):
        assert origin_state in range(self.num_states), f"the value of origin_state ({origin_state}) is out of bounds: [0, {self.num_states-1}]"
        assert end_state in range(self.num_states), f"the value of end_state ({end_state}) is out of bounds: [0, {self.num_states-1}]"
        assert isinstance(input_symbols, str) or isinstance(input_symbols, list) and all(isinstance(c, str) for c in input_symbols), f"The parameter 'characters' should be either a string or a list, you entered {type(input_symbols)}"
        assert input_symbols in self.alphabet if isinstance(input_symbols, str) else all(c in self.alphabet for c in input_symbols), f"The value of the parameter 'characters' is not a subset of the alphabet: {self.alphabet}"
        
        if isinstance(input_symbols, str):
            self.transitions[(origin_state, input_symbols)] = end_state
        elif isinstance(input_symbols, list):
            for c in input_symbols:
                self.transitions[(origin_state, c)] = end_state

    def add_transitions(self, transitions:list[tuple]):
        for t in transitions:
            self.add_transition(t[0], t[1], t[2])

class DFA(FiniteAutomaton):
    def run(self, in_string):
        assert isinstance(in_string, str), "The parameter 'in_string' is not a string (type str)"
        self.current_state = 0
        for c in in_string:
            if (self.current_state, c) in self.transitions.keys():
                self.current_state = self.transitions[(self.current_state, c)]
            else:
                return None #implies error
            
        if self.current_state in self.final_states:
            return True
        else:
            return False

    def next(self, in_string):
        assert isinstance(in_string, str), "The parameter 'in_string' is not a string (type str)"
        for c in in_string:
            if (self.current_state, c) in self.transitions.keys():
                self.current_state = self.transitions[(self.current_state, c)]
            else:
                return None #implies error
            
        return self.current_state

    def run(self, in_string):
        self.current_state = 0
        self.next(in_string)
        if self.current_state in self.final_states:
            return True
        else:
            return False


class NFA(FiniteAutomaton):

    def __init__(self, num_states: int | list[int], alphabet:str | list[str], final_states=[]):
        super().__init__(num_states, alphabet, final_states)
        self.alphabet.append(None)

    def add_transition(self, origin_state:int, end_states:set[int], input_symbols:str | list[str] | None):
        assert origin_state in range(self.num_states), f"the value of origin_state ({origin_state}) is out of bounds: [0, {self.num_states-1}]"
        assert isinstance(end_states, set), "end_states must be a set of integers"
        assert all(n in range(self.num_states) for n in end_states), f"the value of an end_state is out of bounds: [0, {self.num_states-1}]"
        assert input_symbols is None or isinstance(input_symbols, str) or isinstance(input_symbols, list) and all(isinstance(c, str) for c in input_symbols), f"The parameter 'input_symbols' should be either a string or a list, you entered {type(input_symbols)}"
        assert all(c in self.alphabet for c in input_symbols) if isinstance(input_symbols, list) else input_symbols in self.alphabet, f"The value of the parameter 'input_symbols' is not a subset of the alphabet: {self.alphabet}"
        
        if isinstance(input_symbols, list):
            for c in input_symbols:
                self.transitions[(origin_state, c)] = end_states
        else:
            self.transitions[(origin_state, input_symbols)] = end_states

    def null_closure(self, states: set[int], reached=None):
        assert all(n in range(self.num_states) for n in states), f"An accept state is out of bounds: [0, {self.num_states-1}]"
        # Having an empty set as a default parameter value for 'reached' doesn't work, as 'reached' acts as a static variable and isn't assign a new instance of 'set' each time
        # this method is called, but rather it is assigned a new instance on the very first call and the subsequent method calls use the same instance
        if reached is None:
            reached = set()
        closure = states.copy()
        reached.update(closure)
        for state in states:
            if (state, None) in self.transitions:
                closure.update(self.null_closure(self.transitions[(state, None)]-reached, reached))
        return closure
        
    def run(self, in_string):
        s = self.null_closure({0})
        for c in in_string:
            moves = set()
            for state in s:
                if (state, c) in self.transitions:
                    moves.update(self.transitions[(state, c)])
            s = self.null_closure(moves)

        return len(s.intersection(self.final_states)) != 0

    def generate_dfa(self):
        dfa_alpha = self.alphabet[:]
        dfa_alpha.remove(None)
        dfa_states = []
        dfa_transitions = {}
        dfa_states.append(self.null_closure({0}))
        for idx, dfa_state in enumerate(dfa_states):
            for c in dfa_alpha:
                nxt_state = set()
                for nfa_state in dfa_state:
                    if (nfa_state, c) in self.transitions:
                        nxt_state.update(self.null_closure(self.transitions[(nfa_state, c)]))
                if nxt_state not in dfa_states:
                    dfa_states.append(nxt_state)
                dfa_transitions[(idx, c)] = dfa_states.index(nxt_state)

        dfa_final_states = []
        for i, state in enumerate(dfa_states):
            if len(state.intersection(self.final_states)) != 0:
                dfa_final_states.append(i)
        
        dfa = DFA(len(dfa_states), dfa_alpha, dfa_final_states)
        dfa.transitions = dfa_transitions
        return dfa

                             






