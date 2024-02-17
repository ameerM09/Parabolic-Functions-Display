import pygame
import os

pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

WIN_WIDTH = 600
WIN_HEIGHT = 500
CAPTION = "Quadratics and Parabolic Functions"

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(CAPTION)

FPS = 60

PI = 3.14159

BASKETBALL_IMG_WIDTH = 40
BASKETBALL_IMG_HEIGHT = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (185, 185, 180)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 205, 235)
GREEN = (0, 255, 0)
PURPLE = (80, 0, 215)

PLAYER_MAN_WIDTH = 52.5
PLAYER_MAN_HEIGHT = 125

PLAYER_BASKETBALL = pygame.transform.scale(pygame.image.load(os.path.join("assets/player_ball.png")), (BASKETBALL_IMG_WIDTH, BASKETBALL_IMG_HEIGHT))

PLAYER_MAN1 = pygame.transform.scale(pygame.image.load(os.path.join("assets/player_man1.png")), (PLAYER_MAN_WIDTH, PLAYER_MAN_HEIGHT))

UP_ARROW = pygame.image.load(os.path.join("assets/up_arrow.png"))
DOWN_ARROW = pygame.image.load(os.path.join("assets/down_arrow.png"))
RIGHT_ARROW = pygame.image.load(os.path.join("assets/right_arrow.png"))
LEFT_ARROW = pygame.image.load(os.path.join("assets/left_arrow.png"))

def return_font(font_size):
    return pygame.font.SysFont("Comicsans", font_size)

class Basketball():
    ASSET = PLAYER_BASKETBALL

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.asset = self.ASSET

    def draw(self, win, x_offset, y_offset):
        win.blit(self.asset, (self.x + x_offset, self.y + y_offset))

    def draw_parabola(self, win, x_val1, x_val2, y_val1, y_val2):
        # x_val1 = WIN_WIDTH // 2
        # y_val1 = WIN_HEIGHT // 2 - 150
        
        # x_val2 = 100
        # y_val2 = 300

        pygame.draw.arc(win, RED, (x_val1, y_val1, x_val2, y_val2), 0, PI, width = 4)

        """

        Third argument of pygame.draw.arc is the rectangle that the shape is going to be within (data type is tuple):
        (x-position of point, y-position of point), 
        (width that the arc is going to be extruded by, height that the arc is going to be extruded by)

        """

class TextButton():
    def __init__(self, x, y, width, height, color, text=None, text_color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        # Optional parameters, specifically for the erase and clear buttons, as they contain text
        self.text = text
        self.text_color = text_color
        self.clicked = False

    def update_operation(self, win):

        # Creates boxes with outlines around the buttons
        self.main_btn = pygame.draw.rect(win, self.color, ((self.x, self.y), (self.width, self.height)))

        pygame.draw.rect(win, BLACK, ((self.x, self.y), (self.width, self.height)), 2)

        if self.text:
            button_font = return_font(20)

            render_font_surface = button_font.render(self.text, 1, self.text_color)
            win.blit(render_font_surface, (self.x + self.width // 2 - (render_font_surface.get_width() // 2), self.y + self.height // 2 - (render_font_surface.get_height() // 2)))

    def check_for_click(self):
        action = False

        cursor_pos = pygame.mouse.get_pos()

        if self.main_btn.collidepoint(cursor_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        return action

def interactive_bar_functionality(win, basketball, init_x_val2, init_y_val2):
    interactive_bar = pygame.Rect((0, WIN_HEIGHT - 100), (WIN_WIDTH, 100))
    pygame.draw.rect(win, GRAY, interactive_bar)

    cursor_pos = pygame.mouse.get_pos()

    arc_changing_btns = []
    
    initial_x_pos = WIN_WIDTH // 2 - 110

    btn_numbers = []

    for btn_number in range(1, 7):
        btn_numbers.append(str(btn_number))

    for btn_number in btn_numbers:
        btn = TextButton(initial_x_pos, WIN_HEIGHT - 75, 25, 50, WHITE, btn_number)

        initial_x_pos = initial_x_pos + 40

        arc_changing_btns.append(btn)

    if pygame.mouse.get_pressed()[0]:
        cursor_pos = pygame.mouse.get_pos()
    
    for arc_changing_btn in arc_changing_btns:
        arc_changing_btn.update_operation(win)

        if arc_changing_btn.check_for_click():
            for num in range(1, 7):
                if arc_changing_btn.text == str(num):
                    basketball.draw_parabola(win, WIN_WIDTH // 2, init_x_val2, WIN_HEIGHT // 2 - 150, init_y_val2)

                    init_x_val2 = init_x_val2 + 50
                    init_y_val2 = init_y_val2 - 50

def draw_grid(win, rows, width):
    size_btwn = width // rows

    x = 0
    y = 0

    for pos in range(rows):
        x = x + size_btwn
        y = y + size_btwn

        pygame.draw.line(win, (WHITE), (x, 0), (x, width), width = 2)
        pygame.draw.line(win, (WHITE), (0, y), (width, y), width = 2)

def game_loop():
    run = True
    refresh_rate = pygame.time.Clock()

    basketball = Basketball(WIN_WIDTH // 2, WIN_HEIGHT // 2 - PLAYER_BASKETBALL.get_height() * 1.25)

    init_x_val2 = 100
    init_y_val2 = 300

    while run:
        refresh_rate.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WIN.fill(SKY_BLUE)

        draw_grid(WIN, 12, WIN_WIDTH)

        basketball.draw(WIN, -PLAYER_BASKETBALL.get_width() // 2, -PLAYER_BASKETBALL.get_height() // 2)

        interactive_bar_functionality(WIN, basketball, init_x_val2, init_y_val2)

        WIN.blit(PLAYER_MAN1, (100, 100))

        pygame.display.update()

if __name__ == "__main__":
    game_loop() 