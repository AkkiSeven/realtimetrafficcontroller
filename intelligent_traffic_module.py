
import random
import pygame

def simulate_traffic_data():
    """Simulates traffic data for each road.""" 
    return {
        "west": random.randint(0, 20),
        "north": random.randint(0, 20),
        "east": random.randint(0, 20),
        "south": random.randint(0, 20)
    }

def update_traffic_intelligently(traffic_lights, traffic_data):
    """Updates traffic lights based on traffic density.""" 
    # Find the road with the maximum traffic
    max_traffic_road = max(traffic_data, key=traffic_data.get)

    # Set all lights to red, then green for the road with max traffic
    for road in traffic_lights:
        traffic_lights[road] = "red"
    traffic_lights[max_traffic_road] = "green"

    return traffic_lights

