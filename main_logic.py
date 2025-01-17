import pygame
import sys
import math
import os
from traffic_lights import draw_vehicle_counts, initialize_screen, draw_all
from traditional_traffic_module import draw_traffic_lights_with_state, update_traffic_system
from intelligent_traffic_module import simulate_traffic_data, update_traffic_intelligently, display_traffic_data


class Button:
    def __init__(self, x, y, width, height, text, font_path, color, hover_color, border_radius=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_path = font_path
        self.font = pygame.font.Font(font_path, 28) if font_path else pygame.font.Font(None, 28)
        self.color = color
        self.hover_color = hover_color
        self.text_surface = None
        self.text_rect = None
        self.hovered = False  # Track if mouse is hovering
        self.border_radius = border_radius

        # Initial text render
        self.render_text()

    def render_text(self):
        """Renders the button text, resizing the font if necessary."""
        font_size = self.font.get_height()  # get the current font size
        while True:
            self.text_surface = self.font.render(self.text, True, (255, 255, 255))
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)

            if self.text_rect.width <= self.rect.width and self.text_rect.height <= self.rect.height:
                break
            else:
                font_size -= 1
                self.font = pygame.font.Font(self.font_path, font_size) if self.font_path else pygame.font.Font(None, font_size)
            self.text_surface = self.font.render(self.text, True, (255, 255, 255)) # Re-render with AA

    def draw(self, surface):
        current_color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        surface.blit(self.text_surface, self.text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def main():
    screen, constants = initialize_screen(screen_caption="AI Traffic Simulation")

    # Example code to show how you can access variables from traffic module
    print("Screen Width: ", constants["SCREEN_WIDTH"])
    print("Road Width H: ", constants["ROAD_WIDTH_H"])

    # Button Settings
    button_width = 250
    button_height = 60
    button_padding = 10  # Spacing from each other and top
    button_spacing = 15  # Spacing between buttons
    
    # Load a font
    # Ensure the font file is in the same directory as your script
    font_path = "Montserrat-VariableFont_wght.ttf"  # Use a relative path
    if not os.path.exists(font_path):
        print("Font not found, using default")
        button_font = None
    else:
        button_font = font_path
        print("Using custom font")

    button_color = (52, 73, 94)  # Dark blue
    button_hover_color = (44, 62, 80)  # Darker blue
    button_border_radius = 7

    # Button Positions
    start_x = constants["WINDOW_WIDTH"] - button_width - button_padding
    start_y = button_padding

    # Buttons
    traditional_button = Button(start_x, start_y, button_width, button_height, "Traditional Traffic System",
                            button_font, button_color, button_hover_color, button_border_radius)
    intelligent_button = Button(start_x, start_y + button_height + button_spacing, button_width,
                            button_height, "Intelligent Traffic System", button_font, button_color, button_hover_color, button_border_radius)

    # Traffic state variables
    countdown_start_time = 0  # time of button click
    countdown_duration = 10 * 1000 # 10 seconds in ms
    current_road_index = 0
    road_order = ["west", "north", "east", "south"]
    active_system = None # Track which system is running or None if not running
    traffic_lights = {"west": "red", "north": "red", "east": "red", "south": "red"} # Traffic light status

    
    def update_traffic_system(traffic_lights, road_order, road_index):
      for key in traffic_lights:
        traffic_lights[key] = "red"
      traffic_lights[road_order[road_index]] = "green"
      return traffic_lights

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                traditional_button.check_hover(mouse_pos)
                intelligent_button.check_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if traditional_button.check_click(mouse_pos):
                    print("Traditional Button Clicked")
                    active_system = "traditional"
                    countdown_start_time = pygame.time.get_ticks()
                    current_road_index = 0
                    traffic_lights = update_traffic_system(traffic_lights, road_order, current_road_index)
                elif intelligent_button.check_click(mouse_pos):
                    print("Intelligent Button Clicked")
                    active_system = "intelligent"
                    countdown_start_time = pygame.time.get_ticks()
                    traffic_data = simulate_traffic_data()
                    traffic_lights = update_traffic_intelligently(traffic_lights, traffic_data) # To stop the traditional system

        # Draw the traffic system
        screen.fill((232, 255, 239))
        draw_all(screen, constants)
        
        # Draw timer if traditional system is active
        if active_system == "traditional":
          elapsed_time = pygame.time.get_ticks() - countdown_start_time
          remaining_time = max(0, countdown_duration - elapsed_time) # Remaining time
          if remaining_time <=0:
            current_road_index = (current_road_index+1) % 4 # Reset timer and move to next road
            traffic_lights = update_traffic_system(traffic_lights, road_order, current_road_index)
            countdown_start_time = pygame.time.get_ticks()

          font = pygame.font.Font(None, 36)
          timer_text = font.render(f"Time Remaining: {remaining_time // 1000 + 1}", True, (0, 0, 0))
          timer_rect = timer_text.get_rect(topleft=(10,10))
          screen.blit(timer_text, timer_rect)
          draw_traffic_lights_with_state(screen, constants, traffic_lights)
        elif active_system == "intelligent":

            elapsed_time = pygame.time.get_ticks() - countdown_start_time
            remaining_time = max(0, countdown_duration - elapsed_time)
            if remaining_time <= 0:
                traffic_data = simulate_traffic_data()
                traffic_lights = update_traffic_intelligently(traffic_lights, traffic_data)
                countdown_start_time = pygame.time.get_ticks()

            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Intelligent Mode Active", True, (0, 0, 0))
            timer_rect = timer_text.get_rect(topleft=(10, 10))
            screen.blit(timer_text, timer_rect)
            display_traffic_data(screen, traffic_data,constants)
            draw_vehicle_counts(screen, traffic_data,constants)
            draw_traffic_lights_with_state(screen, constants, traffic_lights)

        
        else: # if no traffic is enabled, use default light colors for all
            traffic_lights = {"west": "red", "north": "red", "east": "red", "south": "red"}
            draw_traffic_lights_with_state(screen, constants, traffic_lights)


        # Draw the buttons
        traditional_button.draw(screen)
        intelligent_button.draw(screen)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()