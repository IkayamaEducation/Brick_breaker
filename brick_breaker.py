"""
BRICK BREAKER
Proyek Edukasi Gratis

Hanya untuk penggunaan edukasi pribadi dan non-komersial.
Disediakan "SEBAGAIMANA ADANYA" (AS IS), tanpa jaminan.
Lihat README untuk ketentuan penggunaan dan perizinan.

© 2026 Ikayama Education (PT IKAYAMA MANUSA SOLUSI)
"""

import pygame
import sys


# Window settings.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game colors.
BLACK = (25, 25, 30)
WHITE = (245, 245, 245)

# Each row of bricks has its own color.
BRICK_COLORS = [
    (231, 76, 60),    # Red
    (230, 126, 34),   # Orange
    (241, 196, 15),   # Yellow
    (46, 204, 113),   # Green
    (52, 152, 219)    # Blue
]


def create_bricks():
    bricks = []

    brick_rows = 5
    brick_columns = 8
    brick_width = 86
    brick_height = 25
    brick_gap = 8
    left_margin = 50
    top_margin = 60

    # Place bricks in rows and columns.
    for row in range(brick_rows):
        for column in range(brick_columns):
            x = left_margin + column * (brick_width + brick_gap)
            y = top_margin + row * (brick_height + brick_gap)

            brick = pygame.Rect(x, y, brick_width, brick_height)
            brick_color = BRICK_COLORS[row]
            bricks.append((brick, brick_color))

    return bricks


def main():
    pygame.init()

    # Create the game window.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 64)

    # Create the paddle and ball.
    paddle = pygame.Rect(
        SCREEN_WIDTH // 2 - 55,
        SCREEN_HEIGHT - 50,
        110,
        15
    )
    ball = pygame.Rect(392, 392, 16, 16)

    # Store positions as decimals so small movements are not lost.
    paddle_x = float(paddle.x)
    ball_x = float(ball.x)
    ball_y = float(ball.y)

    # Movement speeds are measured in pixels per second.
    paddle_speed = 420
    ball_speed_x = 300
    ball_speed_y = -300

    score = 0
    lives = 3
    bricks = create_bricks()

    game_active = True
    end_message = ""
    running = True

    # Main game loop.
    while running:
        # Calculate the time passed since the previous frame, in seconds.
        dt = clock.tick(60) / 1000

        # Handle events such as closing the window or pressing a key.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_active and event.key == pygame.K_r:
                    # Reset the game so the player can play again.
                    paddle_x = float(SCREEN_WIDTH // 2 - paddle.width // 2)
                    paddle.x = round(paddle_x)

                    ball_x = float(SCREEN_WIDTH // 2 - ball.width // 2)
                    ball_y = 400 - ball.height / 2
                    ball.x = round(ball_x)
                    ball.y = round(ball_y)

                    ball_speed_x = 300
                    ball_speed_y = -300
                    score = 0
                    lives = 3
                    bricks = create_bricks()
                    game_active = True
                    end_message = ""

        # Update the game while the player is still playing.
        if game_active:
            keys = pygame.key.get_pressed()

            # Move the paddle with the arrow keys or A and D.
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle_x -= paddle_speed * dt
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle_x += paddle_speed * dt

            # Keep the paddle inside the window.
            if paddle_x < 0:
                paddle_x = 0
            if paddle_x + paddle.width > SCREEN_WIDTH:
                paddle_x = SCREEN_WIDTH - paddle.width

            paddle.x = round(paddle_x)

            # Move the ball using the time passed since the previous frame.
            ball_x += ball_speed_x * dt
            ball_y += ball_speed_y * dt
            ball.x = round(ball_x)
            ball.y = round(ball_y)

            # Bounce the ball off the left and right walls.
            if ball.left <= 0:
                ball_x = 0
                ball_speed_x = abs(ball_speed_x)
            if ball.right >= SCREEN_WIDTH:
                ball_x = SCREEN_WIDTH - ball.width
                ball_speed_x = -abs(ball_speed_x)

            # Bounce the ball off the top of the window.
            if ball.top <= 0:
                ball_y = 0
                ball_speed_y = abs(ball_speed_y)

            ball.x = round(ball_x)
            ball.y = round(ball_y)

            # Bounce the ball off the paddle.
            if ball.colliderect(paddle) and ball_speed_y > 0:
                ball_y = paddle.top - ball.height
                ball_speed_y = -abs(ball_speed_y)
                ball.y = round(ball_y)

            # Check whether the ball hits a brick.
            for brick, brick_color in bricks:
                if ball.colliderect(brick):
                    bricks.remove((brick, brick_color))
                    ball_speed_y *= -1
                    score += 10
                    break

            # Check whether the ball has fallen below the paddle.
            if ball.top > SCREEN_HEIGHT:
                lives -= 1

                if lives > 0:
                    # Put the ball back in its starting position.
                    ball_x = float(SCREEN_WIDTH // 2 - ball.width // 2)
                    ball_y = 400 - ball.height / 2
                    ball.x = round(ball_x)
                    ball.y = round(ball_y)
                    ball_speed_x = 300
                    ball_speed_y = -300
                else:
                    game_active = False
                    end_message = "Game Over!"

            # The player wins when all bricks have been removed.
            if len(bricks) == 0:
                game_active = False
                end_message = "You Win!"

        # Draw the background and all game objects.
        screen.fill(BLACK)

        # Draw the bricks in their assigned colors.
        for brick, brick_color in bricks:
            pygame.draw.rect(screen, brick_color, brick)
            pygame.draw.rect(screen, BLACK, brick, 2)

        # Draw the paddle and ball.
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Display the score and remaining lives.
        score_text = font.render("Score: " + str(score), True, WHITE)
        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(score_text, (20, 15))
        screen.blit(lives_text, (680, 15))

        # Display a message when the game ends.
        if not game_active:
            message_text = big_font.render(end_message, True, WHITE)
            restart_text = font.render("Press R to play again", True, WHITE)

            screen.blit(
                message_text,
                message_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            )
            screen.blit(
                restart_text,
                restart_text.get_rect(center=(SCREEN_WIDTH // 2, 335))
            )

        # Update the display.
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()