def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]],
) -> tuple[int, int]:
    current_round = len(my_history.get(opponent_id, []))

    # First move cooperation
    if current_round == 0:
        return 1, 10  # Cooperate and propose 10 rounds initially

    # Helper functions
    def detect_pattern(hist, length=3):
        if len(hist) < length * 2:
            return False, None
        for i in range(len(hist) - length * 2 + 1):
            pattern = hist[i : i + length]
            next_seq = hist[i + length : i + length * 2]
            if pattern == next_seq:
                return True, pattern
        return False, None

    def is_tit_for_tat(my_hist, opp_hist):
        if len(opp_hist) < 3 or opp_hist[0] != 1:
            return False
        matches = 0
        for i in range(1, len(my_hist)):
            if opp_hist[i] == my_hist[i - 1]:
                matches += 1
        return matches >= (len(my_hist) - 1) * 0.9

    def is_random(opp_hist):
        if len(opp_hist) < 15:
            return False
        ones = opp_hist.count(1)
        proportion = ones / len(opp_hist)
        return 0.4 <= proportion <= 0.6

    def detect_exploitation(my_hist, opp_hist):
        if len(my_hist) < 10:
            return False
        defect_after_coop = 0
        coop_count = 0
        for i in range(len(my_hist) - 1):
            if my_hist[i] == 1:
                coop_count += 1
                if opp_hist[i + 1] == 0:
                    defect_after_coop += 1
        return coop_count > 0 and defect_after_coop / coop_count > 0.6

    # Retrieve opponent's history
    opp_history = opponents_history.get(opponent_id, [])
    my_own_history = my_history.get(opponent_id, [])

    # Strategy detection and response
    if is_tit_for_tat(my_own_history, opp_history):
        return 1, 20  # Play longer if opponent is friendly

    if is_random(opp_history):
        return 0, 5  # Short engagement with random behavior

    if detect_exploitation(my_own_history, opp_history):
        return 0, 1  # Minimal play if being exploited

    # Pattern detection and exploitation
    has_pattern, pattern = detect_pattern(opp_history, 3)
    if has_pattern and pattern:
        next_predicted = pattern[current_round % len(pattern)]
        move = 1 if next_predicted == 1 else 0
        return move, 15  # Moderate rounds if predictable

    # Recent behavior analysis
    recent_window = min(10, len(opp_history))
    recent_opponent = opp_history[-recent_window:]
    recent_me = my_own_history[-recent_window:]

    # Quick retaliation for recent defections
    if sum(recent_opponent) == 0:
        return 0, 3

    # Reward mutual cooperation
    if sum(recent_opponent) == recent_window and sum(recent_me) == recent_window:
        return 1, 25

    # Adaptive response
    if opp_history[-1] == 0:
        if sum(opp_history[-3:]) == 0:
            return 0, 3
        if sum(opp_history[-5:]) >= 3:
            return 1, 10
        return 0, 5

    # Strategic defection
    if current_round % 7 == 0:
        return 0, 10

    # Default to cooperation
    return 1, 10
