def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    current_round = len(my_moves)

    if current_round < 2:
        return 1, 1

    if opponent_moves.count(0) >= 3:
        return 0, 0

    total_rounds = max(len(v) for v in my_history.values()) if my_history else None
    if total_rounds is not None and current_round > 0.8 * total_rounds:
        return 0, 0

    recent_opponent_moves = opponent_moves[-5:]
    if 0 in recent_opponent_moves:
        return 0, 0

    return opponent_moves[-1], opponent_moves[-1]
