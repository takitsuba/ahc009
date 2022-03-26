import random


def init_input():
    start_i, start_j, goal_i, goal_j, p = input().split()
    start_i, start_j, goal_i, goal_j = list(
        map(int, (start_i, start_j, goal_i, goal_j))
    )
    p = float(p)

    start = (start_i, start_j)
    goal = (goal_i, goal_j)

    h_walls = []
    for _ in range(20):
        w = [1] + list(map(int, list(input()))) + [1]
        assert len(w) == 21

        h_walls.append(w)

    assert len(h_walls) == 20

    v_walls = []
    v_walls.append([1 for _ in range(20)])
    for _ in range(19):
        w = list(map(int, list(input())))
        assert len(w) == 20

        v_walls.append(w)
    v_walls.append([1 for _ in range(20)])
    assert len(v_walls) == 21

    return start, goal, p, h_walls, v_walls


moves = ["U", "D", "L", "R"]


def main():
    start, goal, p, h_walls, v_walls = init_input()

    print(h_walls)
    print(v_walls)
    print("".join(random.choices(moves, k=100)))


main()
