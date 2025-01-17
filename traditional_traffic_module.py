import pygame
import math
from traffic_lights import draw_rotated_traffic_light, draw_traffic_light_connector

def draw_traffic_lights_with_state(surface, constants, traffic_lights):
    """Draws traffic lights with the specified state."""
    horizontal_light_x_west = constants["INTERSECTION_X1"] - constants["TRAFFIC_LIGHT_OFFSET"] - constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    horizontal_light_y_west = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] // 2
    
    horizontal_light_x_east = constants["INTERSECTION_X2"] + constants["TRAFFIC_LIGHT_OFFSET"] + constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    horizontal_light_y_east = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] // 2

    vertical_light_x_north = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] // 2
    vertical_light_y_north = constants["INTERSECTION_Y1"] - constants["TRAFFIC_LIGHT_OFFSET"] - constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    
    vertical_light_x_south = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] // 2
    vertical_light_y_south = constants["INTERSECTION_Y2"] + constants["TRAFFIC_LIGHT_OFFSET"] + constants["TRAFFIC_LIGHT_HEIGHT"] // 2

    # Draw the traffic lights and their connectors
    draw_rotated_traffic_light_with_state(surface, horizontal_light_x_west, horizontal_light_y_west, -math.pi / 2, traffic_lights["west"], constants)
    draw_traffic_light_connector(surface, (horizontal_light_x_west + constants["TRAFFIC_LIGHT_HEIGHT"]//2, horizontal_light_y_west), (constants["INTERSECTION_X1"], horizontal_light_y_west), constants)
   
    draw_rotated_traffic_light_with_state(surface, horizontal_light_x_east, horizontal_light_y_east, math.pi / 2, traffic_lights["east"], constants)
    draw_traffic_light_connector(surface, (horizontal_light_x_east - constants["TRAFFIC_LIGHT_HEIGHT"]//2, horizontal_light_y_east), (constants["INTERSECTION_X2"], horizontal_light_y_east), constants)

    draw_rotated_traffic_light_with_state(surface, vertical_light_x_north, vertical_light_y_north, math.pi, traffic_lights["north"], constants)
    draw_traffic_light_connector(surface, (vertical_light_x_north, vertical_light_y_north + constants["TRAFFIC_LIGHT_HEIGHT"]//2), (vertical_light_x_north, constants["INTERSECTION_Y1"]), constants)

    draw_rotated_traffic_light_with_state(surface, vertical_light_x_south, vertical_light_y_south, 0, traffic_lights["south"], constants)
    draw_traffic_light_connector(surface, (vertical_light_x_south, vertical_light_y_south - constants["TRAFFIC_LIGHT_HEIGHT"]//2), (vertical_light_x_south, constants["INTERSECTION_Y2"]), constants)


def draw_rotated_traffic_light_with_state(surface, x, y, angle, state, constants):
  traffic_light_surface = pygame.Surface((constants["TRAFFIC_LIGHT_WIDTH"], constants["TRAFFIC_LIGHT_HEIGHT"]), pygame.SRCALPHA)
  pygame.draw.rect(traffic_light_surface, constants["BLACK"], (0, 0, constants["TRAFFIC_LIGHT_WIDTH"], constants["TRAFFIC_LIGHT_HEIGHT"]))
  
  if state == "red":
    pygame.draw.circle(traffic_light_surface, constants["RED"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] // 3 - 5), constants["LIGHT_RADIUS"])
  elif state == "green":
      pygame.draw.circle(traffic_light_surface, constants["GREEN"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] * 2 // 3 + 5), constants["LIGHT_RADIUS"])
  elif state == "yellow":
    pygame.draw.circle(traffic_light_surface, constants["YELLOW"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] * 2 // 3 + 5), constants["LIGHT_RADIUS"])
  else: # Default green
    pygame.draw.circle(traffic_light_surface, constants["GREEN"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] * 2 // 3 + 5), constants["LIGHT_RADIUS"])


  rotated_surface = pygame.transform.rotate(traffic_light_surface, math.degrees(angle))
  rotated_rect = rotated_surface.get_rect(center=(x, y))
  surface.blit(rotated_surface, rotated_rect)


def update_traffic_system(traffic_lights, road_order, road_index):
    for key in traffic_lights:
        traffic_lights[key] = "red"
    traffic_lights[road_order[road_index]] = "green"
    return traffic_lights