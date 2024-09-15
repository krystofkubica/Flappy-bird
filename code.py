import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200  
PIPE_DISTANCE = 300  
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Load images
bird_image = pygame.transform.scale(pygame.image.load("bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))
background_image = pygame.transform.scale(pygame.image.load("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top = self.height - PIPE_HEIGHT
        self.bottom = self.height + PIPE_GAP
        self.passed = False  # Add a flag to check if the pipe has been passed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.top, PIPE_WIDTH, PIPE_HEIGHT))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, PIPE_WIDTH, PIPE_HEIGHT))

    def update(self):
        self.x -= 5

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        if bird.y < self.height or bird.y > self.height + PIPE_GAP:
            if bird.x + BIRD_WIDTH > self.x and bird.x < self.x + PIPE_WIDTH:
                return True
        return False

# Display death screen
def death_screen():
    screen.fill(BLACK)
    death_font = pygame.font.SysFont(None, 72, bold=True)
    death_text = death_font.render("You Died", True, WHITE)
    text_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(death_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds

# Main game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True

    while running:
        clock.tick(30)
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()
        bird.draw()

        if pipes[-1].x < SCREEN_WIDTH - PIPE_DISTANCE:
            pipes.append(Pipe(SCREEN_WIDTH))

        for pipe in pipes:
            pipe.update()
            pipe.draw()
            if pipe.collide(bird):
                running = False
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        score_text = pygame.font.SysFont(None, 36).render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # Display death screen and restart the game
    death_screen()
    main()

if __name__ == "__main__":
    main()