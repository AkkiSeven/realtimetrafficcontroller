import pygame
import math

# Initialize Pygame
pygame.init()

def initialize_screen(screen_caption="Traffic Intersection"):
    """Initializes the pygame screen, taking in an optional screen caption"""
    # --- Constants ---
    # Screen
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h

    # Menu Bar Height (estimated, might need adjustment)
    MENU_BAR_HEIGHT = 25

    # Window Size
    WINDOW_WIDTH = SCREEN_WIDTH
    WINDOW_HEIGHT = SCREEN_HEIGHT - MENU_BAR_HEIGHT

    # Window Position
    WINDOW_X = 0
    WINDOW_Y = 0

    # Base Dimensions (for scaling)
    BASE_WIDTH = 900
    BASE_HEIGHT = 800

    # Scaling Factor
    SCALE_WIDTH = WINDOW_WIDTH / BASE_WIDTH
    SCALE_HEIGHT = WINDOW_HEIGHT / BASE_HEIGHT

    def scale_value(value, isWidth=True):
      if isWidth:
        return int(value * SCALE_WIDTH)
      return int(value * SCALE_HEIGHT)

    # Colors
    GRAY = (71, 71, 71)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
      
    # Road
    ROAD_WIDTH_H = scale_value(200, False)
    ROAD_WIDTH_V = scale_value(200)
    LANE_WIDTH = scale_value(50)
    DASH_LENGTH = scale_value(20)
    DASH_SPACE = scale_value(20)
    LINE_THICKNESS = scale_value(3)

    # Intersection
    INTERSECTION_X1 = scale_value(350)
    INTERSECTION_X2 = scale_value(550)
    INTERSECTION_Y1 = scale_value(300, False)
    INTERSECTION_Y2 = scale_value(500, False)

    # Traffic Lights
    LIGHT_RADIUS = scale_value(15)
    TRAFFIC_LIGHT_WIDTH = scale_value(50)
    TRAFFIC_LIGHT_HEIGHT = scale_value(90)
    TRAFFIC_LIGHT_OFFSET = scale_value(20)
    ROTATE_ANGLE = -math.pi / 2
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(screen_caption)
     
    # Set the window position
    screen_rect = screen.get_rect()
    screen_rect.topleft = (WINDOW_X, WINDOW_Y)
    pygame.display.set_mode(screen_rect.size, pygame.RESIZABLE)

    constants = {
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,
        "WINDOW_WIDTH": WINDOW_WIDTH,
        "WINDOW_HEIGHT": WINDOW_HEIGHT,
        "GRAY": GRAY,
        "WHITE": WHITE,
        "YELLOW": YELLOW,
        "RED": RED,
        "GREEN": GREEN,
        "BLACK": BLACK,
        "ROAD_WIDTH_H": ROAD_WIDTH_H,
        "ROAD_WIDTH_V": ROAD_WIDTH_V,
        "LANE_WIDTH": LANE_WIDTH,
        "DASH_LENGTH": DASH_LENGTH,
        "DASH_SPACE": DASH_SPACE,
        "LINE_THICKNESS": LINE_THICKNESS,
        "INTERSECTION_X1": INTERSECTION_X1,
        "INTERSECTION_X2": INTERSECTION_X2,
        "INTERSECTION_Y1": INTERSECTION_Y1,
        "INTERSECTION_Y2": INTERSECTION_Y2,
        "LIGHT_RADIUS": LIGHT_RADIUS,
        "TRAFFIC_LIGHT_WIDTH": TRAFFIC_LIGHT_WIDTH,
        "TRAFFIC_LIGHT_HEIGHT": TRAFFIC_LIGHT_HEIGHT,
        "TRAFFIC_LIGHT_OFFSET": TRAFFIC_LIGHT_OFFSET,
        "ROTATE_ANGLE": ROTATE_ANGLE,
    }
    
    return screen, constants

# --- Helper Functions ---
def draw_dashed_line(surface, color, start_pos, end_pos, dash_length, space_length, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = (dx ** 2 + dy ** 2) ** 0.5
    dash_count = int(distance / (dash_length + space_length))

    if dash_count <= 0:
        return

    for i in range(dash_count):
        start = (x1 + (dx * (dash_length + space_length) * i) / distance,
                y1 + (dy * (dash_length + space_length) * i) / distance)
        end = (x1 + (dx * (dash_length + space_length) * i + dx * dash_length) / distance,
              y1 + (dy * (dash_length + space_length) * i + dy * dash_length) / distance)
        pygame.draw.line(surface, color, start, end, thickness)


def draw_rotated_traffic_light(surface, x, y, angle, constants):
    traffic_light_surface = pygame.Surface((constants["TRAFFIC_LIGHT_WIDTH"], constants["TRAFFIC_LIGHT_HEIGHT"]), pygame.SRCALPHA)
    pygame.draw.rect(traffic_light_surface, constants["BLACK"], (0, 0, constants["TRAFFIC_LIGHT_WIDTH"], constants["TRAFFIC_LIGHT_HEIGHT"]))
    pygame.draw.circle(traffic_light_surface, constants["RED"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] // 3 - 5), constants["LIGHT_RADIUS"])
    pygame.draw.circle(traffic_light_surface, constants["GREEN"], (constants["TRAFFIC_LIGHT_WIDTH"] // 2, constants["TRAFFIC_LIGHT_HEIGHT"] * 2 // 3 + 5), constants["LIGHT_RADIUS"])

    rotated_surface = pygame.transform.rotate(traffic_light_surface, math.degrees(angle))
    rotated_rect = rotated_surface.get_rect(center=(x, y))
    surface.blit(rotated_surface, rotated_rect)


def draw_traffic_light_connector(surface, start_pos, end_pos, constants):
        pygame.draw.line(surface, constants["BLACK"], start_pos, end_pos, constants["LINE_THICKNESS"])

# --- Drawing Functions ---
def draw_intersection(surface, constants):
    pygame.draw.rect(surface, constants["GRAY"], (0, constants["INTERSECTION_Y1"], constants["WINDOW_WIDTH"], constants["ROAD_WIDTH_H"]))
    pygame.draw.rect(surface, constants["GRAY"], (constants["INTERSECTION_X1"], 0, constants["ROAD_WIDTH_V"], constants["WINDOW_HEIGHT"]))


def draw_horizontal_lanes(surface, constants):
    lane_y1 = constants["INTERSECTION_Y1"] + constants["LANE_WIDTH"]
    lane_y2 = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] - constants["LANE_WIDTH"]

    positions = [
        ((0, lane_y1), (constants["INTERSECTION_X1"], lane_y1)),
        ((0, lane_y2), (constants["INTERSECTION_X1"], lane_y2)),
        ((constants["INTERSECTION_X2"], lane_y1), (constants["WINDOW_WIDTH"], lane_y1)),
        ((constants["INTERSECTION_X2"], lane_y2), (constants["WINDOW_WIDTH"], lane_y2)),
    ]

    for start, end in positions:
        draw_dashed_line(surface, constants["WHITE"], start, end, constants["DASH_LENGTH"], constants["DASH_SPACE"], constants["LINE_THICKNESS"])


def draw_vertical_lanes(surface, constants):
    lane_x1 = constants["INTERSECTION_X1"] + constants["LANE_WIDTH"]
    lane_x2 = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] - constants["LANE_WIDTH"]
    positions = [
        ((lane_x1, 0), (lane_x1, constants["INTERSECTION_Y1"])),
        ((lane_x2, 0), (lane_x2, constants["INTERSECTION_Y1"])),
        ((lane_x1, constants["INTERSECTION_Y2"]), (lane_x1, constants["WINDOW_HEIGHT"])),
        ((lane_x2, constants["INTERSECTION_Y2"]), (lane_x2, constants["WINDOW_HEIGHT"])),
    ]
    for start, end in positions:
        draw_dashed_line(surface, constants["WHITE"], start, end, constants["DASH_LENGTH"], constants["DASH_SPACE"], constants["LINE_THICKNESS"])

def draw_dividers(surface, constants):
    center_y = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] // 2
    center_x = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] // 2

    pygame.draw.line(surface, constants["YELLOW"], (0, center_y), (constants["INTERSECTION_X1"], center_y), constants["LINE_THICKNESS"])
    pygame.draw.line(surface, constants["YELLOW"], (constants["INTERSECTION_X2"], center_y), (constants["WINDOW_WIDTH"], center_y), constants["LINE_THICKNESS"])
    pygame.draw.line(surface, constants["YELLOW"], (center_x, 0), (center_x, constants["INTERSECTION_Y1"]), constants["LINE_THICKNESS"])
    pygame.draw.line(surface, constants["YELLOW"], (center_x, constants["INTERSECTION_Y2"]), (center_x, constants["WINDOW_HEIGHT"]), constants["LINE_THICKNESS"])

def draw_traffic_lights(surface, constants):
    horizontal_light_x_west = constants["INTERSECTION_X1"] - constants["TRAFFIC_LIGHT_OFFSET"] - constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    horizontal_light_y_west = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] // 2
    
    horizontal_light_x_east = constants["INTERSECTION_X2"] + constants["TRAFFIC_LIGHT_OFFSET"] + constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    horizontal_light_y_east = constants["INTERSECTION_Y1"] + constants["ROAD_WIDTH_H"] // 2

    vertical_light_x_north = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] // 2
    vertical_light_y_north = constants["INTERSECTION_Y1"] - constants["TRAFFIC_LIGHT_OFFSET"] - constants["TRAFFIC_LIGHT_HEIGHT"] // 2
    
    vertical_light_x_south = constants["INTERSECTION_X1"] + constants["ROAD_WIDTH_V"] // 2
    vertical_light_y_south = constants["INTERSECTION_Y2"] + constants["TRAFFIC_LIGHT_OFFSET"] + constants["TRAFFIC_LIGHT_HEIGHT"] // 2

    # Draw the traffic lights and their connectors
    draw_rotated_traffic_light(surface, horizontal_light_x_west, horizontal_light_y_west, -math.pi / 2, constants)
    draw_traffic_light_connector(surface, (horizontal_light_x_west + constants["TRAFFIC_LIGHT_HEIGHT"]//2, horizontal_light_y_west), (constants["INTERSECTION_X1"], horizontal_light_y_west), constants)
   
    draw_rotated_traffic_light(surface, horizontal_light_x_east, horizontal_light_y_east, math.pi / 2, constants)
    draw_traffic_light_connector(surface, (horizontal_light_x_east - constants["TRAFFIC_LIGHT_HEIGHT"]//2, horizontal_light_y_east), (constants["INTERSECTION_X2"], horizontal_light_y_east), constants)

    draw_rotated_traffic_light(surface, vertical_light_x_north, vertical_light_y_north, math.pi, constants)
    draw_traffic_light_connector(surface, (vertical_light_x_north, vertical_light_y_north + constants["TRAFFIC_LIGHT_HEIGHT"]//2), (vertical_light_x_north, constants["INTERSECTION_Y1"]), constants)

    draw_rotated_traffic_light(surface, vertical_light_x_south, vertical_light_y_south, 0, constants)
    draw_traffic_light_connector(surface, (vertical_light_x_south, vertical_light_y_south - constants["TRAFFIC_LIGHT_HEIGHT"]//2), (vertical_light_x_south, constants["INTERSECTION_Y2"]), constants)
    

# --- Main Drawing Function ---

def draw_all(surface, constants):
    draw_intersection(surface, constants)
    draw_horizontal_lanes(surface, constants)
    draw_vertical_lanes(surface, constants)
    draw_dividers(surface, constants)
    draw_traffic_lights(surface, constants)