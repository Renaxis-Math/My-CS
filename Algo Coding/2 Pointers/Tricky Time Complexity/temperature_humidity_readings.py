def combine_temp_humidity(temperature_readings, humidity_readings):
    # Time O(n + m) since at any i, j starts at the prev-updated-j -> at any i, j covers a new range of [prev_j ... m]
    # Space O(m) for extra last_humidity dict

    # Worst case time when when all m humidity readings have timestamps <= the last temperature reading's timestamp.
    # Best case time = O(n) when all humidity time > all temperature time
    # Worst case space when all m humidities are for different cities (rare) -> expected space = O(# of unique cities)
 
    answers = []

    last_humidity = {}
    temp_i, hum_j = 0, 0
    while temp_i < len(temperature_readings):
        temp_time, temp_city, temp_value = temperature_readings[temp_i]

        while hum_j < len(humidity_readings) and humidity_readings[hum_j][0] <= temp_time:
            hum_time, hum_city, hum_value = humidity_readings[hum_j]
            last_humidity[hum_city] = hum_value
            hum_j += 1

        if temp_city in last_humidity:
            answers.append((temp_time, temp_city, temp_value, last_humidity[temp_city]))
        else:
            answers.append((temp_time, temp_city, temp_value, None))

        temp_i += 1

    return answers

# Example usage:
temperature_readings = [(2, 'NYC', 68), (6, 'SFO', 73), (11, 'NYC', 65), (13, 'SFO', 75)]
humidity_readings = [(1, 'NYC', 57), (5, 'SFO', 45), (9, 'SFO', 46), (10, 'NYC', 59), (12, 'SFO', 50)]
print(combine_temp_humidity(temperature_readings, humidity_readings))