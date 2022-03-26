import random


def init_input():
    start_i, start_j, goal_i, goal_j, p = input().split()
    start_i, start_j, goal_i, goal_j = list(
        map(int, (start_i, start_j, goal_i, goal_j))
    )
    p = float(p)

    start = (start_i, start_j)
    goal = (goal_i, goal_j)

    def wall_input():
        walls = []
        for _ in range(19):
            w = [1] + list(map(int, list(input()))) + [1]
            walls.append(w)

        return walls

    h_walls = wall_input()
    v_walls = wall_input()

    return start, goal, p, h_walls, v_walls


moves = ["U", "D", "L", "R"]


def main():
    start, goal, p, h_walls, v_walls = init_input()

    print("".join(random.choices(moves, k=100)))


main()
