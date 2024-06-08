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


if __name__ == "__main__":
    main()
    