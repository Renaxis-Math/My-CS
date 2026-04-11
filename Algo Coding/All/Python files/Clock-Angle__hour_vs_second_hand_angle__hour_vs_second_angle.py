def solve_hour_second(time_str: str):
    hour, minute_total, second = _parse_hour_second(time_str) # NEW

    TOTAL_ANGLE_DEG = 360.0

    deg_per_hour = _deg_per_time(TOTAL_ANGLE_DEG, 12)       # 30
    one_hour_deg_per_min = _deg_per_time(deg_per_hour, 60)  # 0.5

    # NEW
    deg_per_sec = _deg_per_time(TOTAL_ANGLE_DEG, 60)        # 6

    second_angle = deg_per_sec * second
    # END NEW
    hour_angle   = deg_per_hour * hour + one_hour_deg_per_min * minute_total

    angle_diff = abs(hour_angle - second_angle)
    return min(angle_diff, TOTAL_ANGLE_DEG - angle_diff)

def _parse_hour_second(time_str: str):
    hour_str, minute_str, second_str = time_str.split(":")
    hour = int(hour_str); minute = int(minute_str); second = float(second_str)

    if not (0 <= hour < 24): raise ValueError("hour must be in [0, 23]")
    if not (0 <= minute < 60): raise ValueError("minute must be in [0, 59]")
    if not (0.0 <= second < 60.0): raise ValueError("second must be in [0, 60)")

    return hour % 12, minute + second / 60.0, second

def _deg_per_time(total_angle_deg, total_time):
    return total_angle_deg / total_time

# -------------------
# TEST
# -------------------

def test():
    
    # 1) Perfect alignment at midnight/noon
    assert solve_hour_second("0:00:00") == 0.0
    assert solve_hour_second("12:00:00") == 0.0
    
    # 2) Maximum possible angle (opposite hands: 180°)
    assert solve_hour_second("3:00:30") == 89.75
    
    # 3) Wrap-around case (close to 360°/0°)
    # Hour at 11:59:59 → 11*30 + 59.983*0.5 = 330 + 29.99 ≈ 359.99°
    # Second at 59 → 354°
    # diff ≈ 5.99°
    assert abs(solve_hour_second("11:59:59") - 5.983333333333333) < 0.01
    
    # 4) 24-hour format wraps correctly (13:00 = 1:00)
    # 13:00:15 same as 1:00:15
    # Hour: 1*30 + 0.25*0.5 = 30.125°
    # Second: 15*6 = 90°
    # diff = 59.875°
    assert solve_hour_second("13:00:15") == 59.875
    
    # 5) Second hand slightly ahead causes small angle
    # 6:30:01 → Hour: 6*30 + 30.016*0.5 ≈ 195.008°
    # Second: 1*6 = 6°
    # diff ≈ 189.008° → smaller = 360-189.008 ≈ 170.99°
    assert abs(solve_hour_second("6:30:01") - 170.99166666666667) < 0.01

test()