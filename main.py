import random
from collections import deque

random.seed(11)


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


def solve_straight(start, goal, h_walls, v_walls):
    """極力直線で。ぶつかったら曲がる"""
    # 今いる場所と向いてる方向ごとに、それに至るまでのrouteを保存する
    visited = [
        [{"U": None, "D": None, "L": None, "R": None} for _ in range(20)]
        for _ in range(20)
    ]
    for direct in moves.keys():
        visited[start[0]][start[1]][direct] = ""

    # 上下左右のスタートの仕方がある
    q = deque([(start, direct) for direct in moves.keys()])

    while q:
        now, direct = q.popleft()
        route = visited[now[0]][now[1]][direct]

        # print(now, direct, route)

        if now == goal:
            return route

        # 200回進んでるのにゴールに辿り着けない場合
        if len(route) >= 200:
            return None

        diff = moves[direct]

        next_i = now[0] + diff[0]
        next_j = now[1] + diff[1]

        if (
            (0 <= next_i <= 19)
            and (0 <= next_j <= 19)
            and visited[next_i][next_j][direct] is not None
        ):
            continue

        if direct in ("U", "D"):
            if direct == "U":
                check_v = now
            else:
                check_v = (now[0] + 1, now[1])

            can_move = v_walls[check_v[0]][check_v[1]] == 0

        if direct in ("L", "R"):
            if direct == "L":
                check_h = now
            else:
                check_h = (now[0], now[1] + 1)

            can_move = h_walls[check_h[0]][check_h[1]] == 0

        # 壁がないので同じ方向に進む
        if can_move:
            assert 0 <= next_i <= 19
            assert 0 <= next_j <= 19
            q.append(((next_i, next_j), direct))
            visited[next_i][next_j][direct] = route + direct

        # 壁がある時だけ方向を変えられる
        else:
            # バックすることは無駄
            if direct in ("U", "D"):
                next_directs = ("L", "R")
            else:
                next_directs = ("U", "D")

            for next_direct in next_directs:
                if visited[now[0]][now[1]][next_direct] is not None:
                    # すでにその場所でその方向を向いて進んだことがあるので pass
                    continue
                else:
                    # そこに至るまでのrouteは変わらない（別の言い方をすれば、ノーアクションで向きを変えることが可能）
                    visited[now[0]][now[1]][next_direct] = route
                    q.append((now, next_direct))


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


def solve_biased_route(start, goal, h_walls, v_walls):
    """ゴールまでの経路の座標をリストで返す
    STARTは含まず、GOALは含む。
    """
    visited = [[None for _ in range(20)] for _ in range(20)]
    visited[start[0]][start[1]] = ""

    q = deque([(start, direct) for direct in moves.keys()])

    while q:
        now, past_direct = q.popleft()
        route = visited[now[0]][now[1]]
        if now == goal:
            return route

        directions = list(moves.keys())
        directions.remove(past_direct)
        biased_directions = [past_direct] + directions

        for direction in biased_directions:
            diff = moves[direction]
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

            if past_direct == direction and not can_move:
                more = True

            if can_move:
                assert 0 <= next_i <= 19
                assert 0 <= next_j <= 19
                q.append(((next_i, next_j), direction))
                if more:
                    visited[next_i][next_j] = route + direction * 3
                else:
                    visited[next_i][next_j] = route + direction
                more = False


def main():
    start, goal, p, h_walls, v_walls = init_input()

    route = solve_straight(start, goal, h_walls, v_walls)

    if route is None:
        # 最短距離の方を使う
        route = solve_biased_route(start, goal, h_walls, v_walls)
        max_add = 200 - len(route)

        redundant = ""
        forget_cnt = 0
        for direction in list(route):
            redundant += direction
            if forget_cnt < max_add and random.uniform(0, 1) < p:
                # 忘れそうなのでもう1回足しておく
                redundant += direction
                forget_cnt += 1

        print(redundant)

    else:
        max_add = 200 - len(route)
        compression = []
        for d in list(route):
            if len(compression) == 0:
                compression.append([d, 1])
                continue
            if compression[-1][0] == d:
                compression[-1][1] += 1
            else:
                compression.append([d, 1])

        # print(compression)
        redundant_compression = []
        for d, cnt in compression:
            cnt += int(max_add * (cnt / len(route)))
            redundant_compression.append([d, cnt])
        # print(redundant_compression)

        redundant = ""
        for d, cnt in redundant_compression:
            redundant += d * cnt

        if len(redundant) > 200:
            print(redundant[:200])
        else:
            print(redundant)


main()
