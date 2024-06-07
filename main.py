import pygame
import random

# Constants
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = 6
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_ADD_INTERVAL = 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel = 0
        self.width = 30
        self.height = 30

    def flap(self):
        self.vel = -FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > HEIGHT or self.y < 0

class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.bottom_height = HEIGHT - PIPE_GAP - self.top_height
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height))

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

    def collides_with_bird(self, bird):
        return (bird.x < self.x + PIPE_WIDTH and bird.x + bird.width > self.x and
                (bird.y < self.top_height or bird.y + bird.height > HEIGHT - self.bottom_height))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    score = 0

    started = False  # Track if the game has started
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:  # Start the game on the first click
                started = True
                bird.flap()

        # Render everything
        screen.fill(WHITE)
        bird.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.flap()

        # Check for collision with pipes
        for pipe in pipes:
            if pipe.collides_with_bird(bird):
                running = False

        # Check for passing pipes and update score
        for pipe in pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                pipe.passed = True
                score += 1

        # Add new pipes
        if pipes and pipes[-1].x < WIDTH - PIPE_ADD_INTERVAL:
            pipes.append(Pipe(WIDTH))
        elif not pipes:
            pipes.append(Pipe(WIDTH))

        # Remove off-screen pipes
        if pipes and pipes[0].is_off_screen():
            pipes.pop(0)

        # Update bird position and pipes
        bird.update()
        for pipe in pipes:
            pipe.move()

        # Draw everything
        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over!")
    print("Your score was:", score)

if __name__ == "__main__":
    main()