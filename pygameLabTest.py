import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GRAVITY = 1
JUMP_STRENGTH = 15
PANEL_WIDTH = 200  # Width of the upgrade panel
MIDDLE_WIDTH = 200  # Width of the middle text column
GAME_WIDTH = WIDTH - PANEL_WIDTH - MIDDLE_WIDTH  # Remaining width for the game area

OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
OBSTACLE_SPEED = 5
SPAWN_INTERVAL = 1500  # milliseconds

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jumping Dino Game')

# Dino class
class Dino:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 50
        self.width = 40
        self.height = 40
        self.vel_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -JUMP_STRENGTH
            self.is_jumping = True
            return True  # Indicate that a jump occurred
        return False

    def update(self):
        self.y += self.vel_y
        if self.is_jumping:
            self.vel_y += GRAVITY

        # Check for landing
        if self.y >= HEIGHT - 50:
            self.y = HEIGHT - 50
            self.is_jumping = False
            self.vel_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))

# Obstacle class
class Obstacle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 50
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT

    def update(self):
        self.x -= OBSTACLE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))

# Upgrade button class
class UpgradeButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game loop
def main():
    clock = pygame.time.Clock()
    dino = Dino()
    obstacles = []
    score = 0
    gold_nuggets = 0
    game_over = False

    # Create upgrade buttons
    buttons = [
        UpgradeButton(WIDTH - PANEL_WIDTH + 20, 50, 160, 40, 'Upgrade 1'),
        UpgradeButton(WIDTH - PANEL_WIDTH + 20, 100, 160, 40, 'Upgrade 2'),
        UpgradeButton(WIDTH - PANEL_WIDTH + 20, 150, 160, 40, 'Upgrade 3'),
    ]

    # Timer for obstacle spawning
    last_spawn_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    if dino.jump():
                        gold_nuggets += 1  # Increment gold nuggets on a successful jump

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        print(f"{button.text} clicked!")

        # Update
        if not game_over:
            dino.update()

            # Update obstacles
            for obstacle in obstacles:
                obstacle.update()
                # Check for collision
                if (dino.x < obstacle.x + obstacle.width and
                    dino.x + dino.width > obstacle.x and
                    dino.y < obstacle.y + obstacle.height and
                    dino.y + dino.height > obstacle.y):
                    game_over = True

            # Remove off-screen obstacles
            obstacles = [obstacle for obstacle in obstacles if obstacle.x > 0]

            # Spawn new obstacles at regular intervals
            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time > SPAWN_INTERVAL:
                obstacles.append(Obstacle(WIDTH - PANEL_WIDTH - 1))  # Spawn just before the right panel
                last_spawn_time = current_time

            score += 1

        # Draw
        screen.fill(WHITE)

        # Draw the game area on the left
        dino.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw the middle column
        middle_x = GAME_WIDTH  # Positioning for the middle column
        pygame.draw.rect(screen, GRAY, (GAME_WIDTH, 0, MIDDLE_WIDTH, HEIGHT))

        font = pygame.font.SysFont(None, 40)
        title_words = ["Adventure", "Clicker"]
        for i, word in enumerate(title_words):
            text_surface = font.render(word, True, BLACK)
            screen.blit(text_surface, (GAME_WIDTH + 10, 50 + i * 50))  # Adjust y-coordinate for each word

        # Separate the gold nuggets display
        nuggets_surface = font.render(f'Gold Nuggets:', True, BLACK)
        screen.blit(nuggets_surface, (GAME_WIDTH + 10, 150))  # Position for gold nuggets label
        nuggets_value_surface = font.render(f'{gold_nuggets}', True, BLACK)
        screen.blit(nuggets_value_surface, (GAME_WIDTH + 10, 200))  # Position for gold nuggets value

        # Draw the panel and buttons on the right
        pygame.draw.rect(screen, BLACK, (WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        for button in buttons:
            button.draw(screen)

        # Game Over screen
        if game_over:
            font = pygame.font.SysFont(None, 50)
            game_over_surface = font.render('Game Over', True, BLACK)
            score_surface = font.render(f'Score: {score}', True, BLACK)
            nuggets_surface = font.render(f'Gold Nuggets: {gold_nuggets}', True, BLACK)
            screen.blit(game_over_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
            screen.blit(score_surface, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
            screen.blit(nuggets_surface, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
