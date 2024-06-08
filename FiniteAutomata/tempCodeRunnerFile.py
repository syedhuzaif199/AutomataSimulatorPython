    n = NFA(7, "ab")
    n.add_transitions([
        (0, {1}, None),
        (1, {2}, None),
        (2, {3}, None),
        (3, {4}, None),
        (4, {0}, None),
        (4, {5}, None),
        (5, {6}, None),
        (4, {2}, None),
    ])