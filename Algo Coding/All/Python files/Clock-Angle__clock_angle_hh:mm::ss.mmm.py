"""
Time Complexity: O(1)
Space Complexity: O(1)
"""
def solve(time_str: str):
    """
    Follow up: input is "H:MM:SS"

    Derivation:
      - Minute hand: 360 degrees / 60 minutes = 6 degrees per minute
      - Hour hand:   360 degrees / 12 hours   = 30 degrees per hour
                    plus it moves continuously: 30/60 = 0.5 degrees per minute
    """
    hour, minute = _parse_follow_up(time_str) # NEW

    TOTAL_ANGLE_DEG = 360.0

    deg_per_hour = _deg_per_time(TOTAL_ANGLE_DEG, 12)       # 30
    one_hour_deg_per_min = _deg_per_time(deg_per_hour, 60)  # 0.5

    deg_per_min = _deg_per_time(TOTAL_ANGLE_DEG, 60)        # 6

    minute_angle = deg_per_min * minute
    hour_angle = deg_per_hour * hour + one_hour_deg_per_min * minute

    angle_diff = abs(hour_angle - minute_angle)
    return min(angle_diff, TOTAL_ANGLE_DEG - angle_diff) # acute angle only

# NEW
def _parse_follow_up(time_str):
    hour_str, minute_str, second = time_str.split(":")
    
    hour = int(hour_str); minute = int(minute_str); second = float(second)
    
    if not (0 <= hour < 24): raise ValueError("hour must be in [0, 23]")
    if not (0 <= minute < 60): raise ValueError("minute must be in [0, 59]")
    if not (0.0 <= second < 60.0): raise ValueError("second must be in [0, 60)")

    return hour % 12, minute + second / 60 # NEW
# END NEW

def _deg_per_time(total_angle_deg, total_time):
    return total_angle_deg / total_time

# -------------------
# TESTS
# -------------------

def test():

    # 1) Midnight exactly: both hands at 12
    assert solve("0:00:00") == 0.0

    # 2) Noon exactly: same as 12 on an analog clock
    assert solve("12:00:00") == 0.0

    # 3) Exact half-turn: 6:00:00 -> hour at 180°, minute at 0° -> 180°
    assert solve("6:00:00") == 180.0

    # 4) 24-hour mapping edge: 15:00:00 == 3:00:00 -> 90°
    assert solve("15:00:00") == 90.0

    # 5) Extreme near wrap: 23:59:59 (tiny angle)
    # Exact value is 11/120 degrees = 0.091666...
    assert abs(solve("23:59:59") - (11/120)) < 1e-12

    # -------------------
    # General test (valid)
    # -------------------

    # 6) Typical nontrivial: 3:45:30
    # minute_total = 45 + 30/60 = 45.5
    # minute_angle = 6*45.5 = 273
    # hour_angle = 30*3 + 0.5*45.5 = 90 + 22.75 = 112.75
    # diff = 160.25
    assert solve("3:45:30") == 160.25

test()