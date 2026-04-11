"""
Time Complexity: O(1)
Space Complexity: O(1)
"""
def solve(time_str: str):
    """
    Given "H:MM" (or "HH:MM"), return the smaller angle (in degrees)
    between the hour and minute hands.

    Derivation:
      - Minute hand: 360 degrees / 60 minutes = 6 degrees per minute
      - Hour hand:   360 degrees / 12 hours   = 30 degrees per hour
                    plus it moves continuously: 30/60 = 0.5 degrees per minute
    """
    hour, minute = _parse(time_str)

    TOTAL_ANGLE_DEG = 360.0

    deg_per_hour = _deg_per_time(TOTAL_ANGLE_DEG, 12)       # 30
    one_hour_deg_per_min = _deg_per_time(deg_per_hour, 60)  # 0.5

    deg_per_min = _deg_per_time(TOTAL_ANGLE_DEG, 60)        # 6

    minute_angle = deg_per_min * minute
    hour_angle = deg_per_hour * hour + one_hour_deg_per_min * minute

    angle_diff = abs(hour_angle - minute_angle)
    return min(angle_diff, TOTAL_ANGLE_DEG - angle_diff) # acute angle only

def _parse(time_str):
    hour_str, minute_str = time_str.split(":")

    hour = int(hour_str); minute = int(minute_str)
    
    if not (0 <= hour < 24): raise ValueError("hour must be in [0, 23]")    
    if not (0 <= minute < 60): raise ValueError("minute must be in [0, 59]")

    return hour % 12, minute

def _deg_per_time(total_angle_deg, total_time):
    return total_angle_deg / total_time


# -------------------
# TEST
# -------------------

def test():

    # 1) Midnight / noon: both hands at 12 -> 0 degrees
    assert solve("0:00") == 0.0
    assert solve("12:00") == 0.0

    # 2) 24-hour mapping: 15:00 == 3:00 -> 90 degrees
    assert solve("15:00") == 90.0

    # 3) Max minute: 23:59 should be very close to 5.5 degrees
    # hour = 11, minute = 59 -> hour_angle=30*11+0.5*59=359.5, minute_angle=354 -> diff=5.5
    assert solve("23:59") == 5.5

    # 4) Typical case: 3:45 -> minute=270, hour=112.5 -> diff=157.5
    assert solve("3:45") == 157.5

test()