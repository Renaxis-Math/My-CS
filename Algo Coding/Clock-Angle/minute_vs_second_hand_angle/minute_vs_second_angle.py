def solve_minute_second(time_str: str):
    _, minute_total, second = _parse_minute_second(time_str) # NEW

    TOTAL_ANGLE_DEG = 360.0

    deg_per_min = _deg_per_time(TOTAL_ANGLE_DEG, 60)  # 6 deg/min
    deg_per_sec = _deg_per_time(TOTAL_ANGLE_DEG, 60)  # 6 deg/sec

    minute_angle = deg_per_min * minute_total
    second_angle = deg_per_sec * second

    angle_diff = abs(minute_angle - second_angle)
    return min(angle_diff, TOTAL_ANGLE_DEG - angle_diff)

def _parse_minute_second(time_str: str):
    hour_str, minute_str, second_str = time_str.split(":")
    hour = int(hour_str)          # not used in this pair, but validate input
    minute = int(minute_str)
    second = float(second_str)    # supports SS.mmm

    if not (0 <= hour < 24): raise ValueError("hour must be in [0, 23]")
    if not (0 <= minute < 60): raise ValueError("minute must be in [0, 59]")
    if not (0.0 <= second < 60.0): raise ValueError("second must be in [0, 60)")

    return hour, minute + second / 60.0, second

def _deg_per_time(total_angle_deg, total_time):
    return total_angle_deg / total_time

# -------------------
# TEST
# -------------------

def test():

    # 1) Exact alignment at start of minute
    assert solve_minute_second("0:00:00") == 0.0

    # 2) Opposite direction half-turn: minute at 0°, second at 180°
    assert solve_minute_second("0:00:30") == 177.0

    # 3) Minute hand advanced by 0.5° at 5 seconds, second hand at 30°
    # minute_total = 0 + 5/60 = 1/12
    # minute_angle = 6*(1/12) = 0.5
    # second_angle = 6*5 = 30
    # diff = 29.5 (smaller angle)
    assert solve_minute_second("0:00:05") == 29.5

    # 4) 24-hour hour field irrelevant (should not affect result)
    assert solve_minute_second("23:00:30") == 177.0

test()