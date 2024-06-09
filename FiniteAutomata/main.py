from FiniteAutomaton import DFA, NFA

def main():
    n = NFA(11, "ab", [10])
    n.add_transitions([
        (0, {1,7}, None),
        (1, {2,4}, None),
        (2, {3}, "a"),
        (3, {6}, None),
        (4, {5}, "b"),
        (5, {6}, None),
        (6, {1,7}, None),
        (7, {8}, "a"),
        (8, {9}, "b"),
        (9, {10}, "b"),
    ])

    dfa = n.generate_dfa()
    print(dfa.transitions)


    dfa2 = DFA(6, "01", [3,5])
    dfa2.add_transitions([
        (0,1,"0"),
        (0,3,"1"),
        (1,0,"0"),
        (1,3,"1"),
        (2,1,"0"),
        (2,4,"1"),
        (3,5,"0"),
        (3,5,"1"),
        (4,3,"0"),
        (4,3,"1"),
        (5,5,"0"),
        (5,5,"1"),
    ])

    min_dfa = dfa2.get_minimized()
    print(min_dfa.num_states)
    print(min_dfa.transitions)
    print(min_dfa.final_states)


if __name__ == "__main__":
    main()
    