from FiniteAutomaton import DFA, NFA

def main():
    
    dfa = DFA(6, "01", [2,3,4])
    dfa.add_transitions([
        (0,1,"0"),
        (0,2,"1"),
        (1,0,"0"),
        (1,3,"1"),
        (2,4,"0"),
        (2,5,"1"),
        (3,4,"0"),
        (3,5,"1"),
        (4,4,"0"),
        (4,5,"1"),
        (5,5,"0"),
        (5,5,"1"),
    ])

    print(dfa.transitions)
    
    min_dfa = dfa.get_minimized()

    print("Number of states:",min_dfa.num_states)
    print("Transitions:",min_dfa.transitions)
    print("Final states:",min_dfa.final_states)


if __name__ == "__main__":
    main()
    