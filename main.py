import random
from collections import deque


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


moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def solve_route(start, goal, h_walls, v_walls):
    """ゴールまでの経路の座標をリストで返す
    STARTは含まず、GOALは含む。
    """
    visited = [[None for _ in range(20)] for _ in range(20)]
    visited[start[0]][start[1]] = ""

    q = deque([start])

    while q:
        now = q.popleft()
        route = visited[now[0]][now[1]]

        if now == goal:
            return route

        for direction, diff in moves.items():
            next_i = now[0] + diff[0]
            next_j = now[1] + diff[1]

            # print(direction, next_i, next_j)
            # そんな場所は存在しないか、
            # すでに行ったことあるなら無視する
            if (
                (0 <= next_i <= 19)
                and (0 <= next_j <= 19)
                and visited[next_i][next_j] is not None
            ):
                continue

            if direction in ("U", "D"):
                if direction == "U":
                    check_v = now
                else:
                    check_v = (now[0] + 1, now[1])

                can_move = v_walls[check_v[0]][check_v[1]] == 0

            if direction in ("L", "R"):
                if direction == "L":
                    check_h = now
                else:
                    check_h = (now[0], now[1] + 1)

                can_move = h_walls[check_h[0]][check_h[1]] == 0

            if can_move:
                assert 0 <= next_i <= 19
                assert 0 <= next_j <= 19
                q.append((next_i, next_j))
                visited[next_i][next_j] = route + direction


def main():
    start, goal, p, h_walls, v_walls = init_input()

    route = solve_route(start, goal, h_walls, v_walls)

    print(route)


main()
