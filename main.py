import cv2
import mediapipe as mp
import pygame
import random
import numpy as np
import sys

# =========================
# CONFIG
# =========================
GAME_WIDTH = 800
CAM_WIDTH = 400
HEIGHT = 600
TOTAL_WIDTH = GAME_WIDTH + CAM_WIDTH

BULLET_SPEED = 10
ENEMY_SPEED = 4
MAX_LIVES = 2
EXIT_HOLD_TIME = 60  # 1 second hold

# =========================
# INIT PYGAME
# =========================
pygame.init()
screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Fighter Shooter")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

# =========================
# LOAD IMAGES
# =========================
fighter_img = pygame.image.load("fighter.png").convert_alpha()
fighter_img = pygame.transform.scale(fighter_img, (80, 60))

enemy_img = pygame.image.load("enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (70, 80))

# =========================
# TOP 5 SCORE SYSTEM
# =========================
def load_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            return [int(score.strip()) for score in scores]
    except:
        return []

def save_scores(scores):
    with open("scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")

def update_top_scores(current_score):
    scores = load_scores()
    scores.append(current_score)
    scores = sorted(scores, reverse=True)[:5]
    save_scores(scores)
    return scores

top_scores = load_scores()

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# =========================
# FUNCTIONS
# =========================
def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

def reset_game():
    player = pygame.Rect(GAME_WIDTH//2, HEIGHT-100, 80, 60)
    return player, [], [], 0, MAX_LIVES

# =========================
# BACKGROUND STARS
# =========================
stars = [(random.randint(0, GAME_WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# =========================
# INITIAL STATE
# =========================
player, bullets, enemies, score, lives = reset_game()
game_state = "MENU"
shoot_cooldown = 0
exit_timer = 0
running = True

# =========================
# MAIN LOOP
# =========================
while running:
    clock.tick(60)
    screen.fill((5, 5, 20))

    # ===== CAMERA =====
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingers = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(hand_landmarks)

            # Highlight fingertip
            tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            cx, cy = int(tip.x * w), int(tip.y * h)
            cv2.circle(frame, (cx, cy), 15, (0,255,255), 3)

            if game_state == "PLAYING":
                player.x = int(hand_landmarks.landmark[9].x * GAME_WIDTH)

    # Clamp player
    player.x = max(0, min(player.x, GAME_WIDTH - 80))

    # =========================
    # SAFE EXIT (MENU ONLY)
    # =========================
    if game_state == "MENU" and fingers == 3:
        exit_timer += 1
        if exit_timer > EXIT_HOLD_TIME:
            running = False
    else:
        exit_timer = 0

    # Convert camera to pygame
    frame = cv2.resize(frame, (CAM_WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    cam_surface = pygame.surfarray.make_surface(frame)

    # ===== STAR BACKGROUND =====
    for i in range(len(stars)):
        pygame.draw.circle(screen, (255,255,255), stars[i], 2)
        stars[i] = (stars[i][0], stars[i][1] + 2)
        if stars[i][1] > HEIGHT:
            stars[i] = (random.randint(0, GAME_WIDTH), 0)

    # =========================
    # MENU STATE
    # =========================
    if game_state == "MENU":
        title = big_font.render("GESTURE FIGHTER", True, (255,255,255))
        start_text = font.render("Show 2 Fingers To Start", True, (0,255,255))
        exit_text = font.render("Hold 3 Fingers To Exit", True, (255,100,100))

        screen.blit(title, (GAME_WIDTH//2 - 180, HEIGHT//2 - 150))
        screen.blit(start_text, (GAME_WIDTH//2 - 150, HEIGHT//2 - 90))
        screen.blit(exit_text, (GAME_WIDTH//2 - 150, HEIGHT//2 - 50))

        # Leaderboard Title
        leaderboard_title = font.render("TOP 5 SCORES", True, (255,255,0))
        screen.blit(leaderboard_title, (GAME_WIDTH//2 - 100, HEIGHT//2))

        # Display Top Scores
        for i, s in enumerate(top_scores):
            score_text = font.render(f"{i+1}. {s}", True, (255,255,255))
            screen.blit(score_text, (GAME_WIDTH//2 - 50, HEIGHT//2 + 40 + i*30))

        if fingers == 2:
            player, bullets, enemies, score, lives = reset_game()
            game_state = "PLAYING"

    # =========================
    # PLAYING STATE
    # =========================
    elif game_state == "PLAYING":

        # Shoot
        if fingers >= 4 and shoot_cooldown <= 0:
            bullets.append(pygame.Rect(player.centerx-5, player.y, 10, 20))
            shoot_cooldown = 15

        # Bullets
        for bullet in bullets:
            bullet.y -= BULLET_SPEED
            pygame.draw.rect(screen, (255,255,0), bullet)
        bullets = [b for b in bullets if b.y > 0]

        # Spawn enemies
        if random.randint(1, 40) == 1:
            enemies.append(pygame.Rect(random.randint(0, GAME_WIDTH-70), -80, 70, 80))

        # Draw enemies
        for enemy in enemies:
            enemy.y += ENEMY_SPEED
            screen.blit(enemy_img, (enemy.x, enemy.y))

        # Collisions
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break

            if enemy.colliderect(player):
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    top_scores = update_top_scores(score)
                    game_state = "MENU"

        enemies = [e for e in enemies if e.y < HEIGHT]

        # Draw player
        screen.blit(fighter_img, (player.x, player.y))

        # Health Bar
        pygame.draw.rect(screen, (100,100,100), (10,10,200,20))
        pygame.draw.rect(screen, (0,255,0), (10,10,200*(lives/MAX_LIVES),20))

        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,40))

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

    # ===== DRAW CAMERA =====
    screen.blit(cam_surface, (GAME_WIDTH, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
pygame.quit()
sys.exit()