# import cv2
# import mediapipe as mp
# import pygame
# import random
# import numpy as np

# # ========================
# # CONFIG
# # ========================
# GAME_WIDTH = 800
# CAM_WIDTH = 400
# HEIGHT = 600
# TOTAL_WIDTH = GAME_WIDTH + CAM_WIDTH

# BULLET_SPEED = 10
# ENEMY_SPEED = 5
# MAX_LIVES = 3

# # ========================
# # INIT PYGAME
# # ========================
# pygame.init()
# screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
# pygame.display.set_caption("Gesture Space Shooter")
# clock = pygame.time.Clock()

# font = pygame.font.SysFont(None, 36)
# big_font = pygame.font.SysFont(None, 60)

# # ========================
# # MEDIAPIPE
# # ========================
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1)
# mp_draw = mp.solutions.drawing_utils
# cap = cv2.VideoCapture(0)

# def count_fingers(hand_landmarks):
#     tips = [8, 12, 16, 20]
#     count = 0
#     for tip in tips:
#         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
#             count += 1
#     return count

# def reset_game():
#     return (
#         pygame.Rect(GAME_WIDTH//2, HEIGHT-80, 60, 40),
#         [],
#         [],
#         0,
#         MAX_LIVES
#     )

# player, bullets, enemies, score, lives = reset_game()
# game_state = "MENU"
# shoot_cooldown = 0

# running = True

# while running:
#     clock.tick(60)
#     screen.fill((10,10,30))

#     # ========================
#     # CAMERA
#     # ========================
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb)

#     fingers = 0

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#             fingers = count_fingers(hand_landmarks)

#             # Highlight fingertip
#             tip = hand_landmarks.landmark[8]
#             h, w, _ = frame.shape
#             cx, cy = int(tip.x * w), int(tip.y * h)
#             cv2.circle(frame, (cx, cy), 15, (0,255,255), 3)

#             if game_state == "PLAYING":
#                 player.x = int(hand_landmarks.landmark[9].x * GAME_WIDTH)

#     # Convert camera to pygame surface
#     frame = cv2.resize(frame, (CAM_WIDTH, HEIGHT))
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = np.rot90(frame)
#     cam_surface = pygame.surfarray.make_surface(frame)

#     # ========================
#     # MENU STATE
#     # ========================
#     if game_state == "MENU":
#         title = big_font.render("GESTURE SPACE SHOOTER", True, (255,255,255))
#         instruction = font.render("Show 2 Fingers To Start", True, (0,255,255))

#         screen.blit(title, (GAME_WIDTH//2 - 250, HEIGHT//2 - 60))
#         screen.blit(instruction, (GAME_WIDTH//2 - 170, HEIGHT//2))

#         if fingers == 2:
#             player, bullets, enemies, score, lives = reset_game()
#             game_state = "PLAYING"

#     # ========================
#     # PLAYING STATE
#     # ========================
#     elif game_state == "PLAYING":

#         if fingers >= 4 and shoot_cooldown <= 0:
#             bullets.append(pygame.Rect(player.centerx-5, player.y, 10, 20))
#             shoot_cooldown = 15

#         for bullet in bullets:
#             bullet.y -= BULLET_SPEED
#             pygame.draw.rect(screen, (255,255,0), bullet)

#         bullets = [b for b in bullets if b.y > 0]

#         if random.randint(1,30) == 1:
#             enemies.append(pygame.Rect(random.randint(0, GAME_WIDTH-40), -50, 40, 40))

#         for enemy in enemies:
#             enemy.y += ENEMY_SPEED
#             pygame.draw.rect(screen, (255,0,0), enemy)

#         for enemy in enemies[:]:
#             for bullet in bullets[:]:
#                 if enemy.colliderect(bullet):
#                     enemies.remove(enemy)
#                     bullets.remove(bullet)
#                     score += 10
#                     break

#             if enemy.colliderect(player):
#                 enemies.remove(enemy)
#                 lives -= 1
#                 if lives <= 0:
#                     game_state = "GAME_OVER"

#         enemies = [e for e in enemies if e.y < HEIGHT]

#         pygame.draw.rect(screen, (0,255,0), player)

#         score_text = font.render(f"Score: {score}", True, (255,255,255))
#         lives_text = font.render(f"Lives: {lives}", True, (255,0,0))

#         screen.blit(score_text, (10,10))
#         screen.blit(lives_text, (10,40))

#         if shoot_cooldown > 0:
#             shoot_cooldown -= 1

#     # ========================
#     # GAME OVER STATE
#     # ========================
#     elif game_state == "GAME_OVER":
#         over_text = big_font.render("GAME OVER", True, (255,0,0))
#         replay_text = font.render("Show 2 Fingers To Replay", True, (0,255,255))

#         screen.blit(over_text, (GAME_WIDTH//2 - 150, HEIGHT//2 - 60))
#         screen.blit(replay_text, (GAME_WIDTH//2 - 170, HEIGHT//2))

#         if fingers == 2:
#             player, bullets, enemies, score, lives = reset_game()
#             game_state = "PLAYING"

#     # ========================
#     # DRAW CAMERA
#     # ========================
#     screen.blit(cam_surface, (GAME_WIDTH, 0))

#     pygame.display.update()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
# import cv2
# import mediapipe as mp
# import pygame
# import random
# import numpy as np

# # =========================
# # CONFIG
# # =========================
# GAME_WIDTH = 800
# CAM_WIDTH = 400
# HEIGHT = 600
# TOTAL_WIDTH = GAME_WIDTH + CAM_WIDTH

# BULLET_SPEED = 10
# ENEMY_SPEED = 5
# MAX_LIVES = 2

# # =========================
# # INIT PYGAME
# # =========================
# pygame.init()
# screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
# pygame.display.set_caption("Gesture Space Shooter")
# clock = pygame.time.Clock()

# font = pygame.font.SysFont("Arial", 28)
# big_font = pygame.font.SysFont("Arial", 60)

# # =========================
# # MEDIAPIPE
# # =========================
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1)
# mp_draw = mp.solutions.drawing_utils
# cap = cv2.VideoCapture(0)

# # =========================
# # UTILITY FUNCTIONS
# # =========================
# def count_fingers(hand_landmarks):
#     tips = [8, 12, 16, 20]
#     count = 0
#     for tip in tips:
#         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
#             count += 1
#     return count

# def reset_game():
#     player = pygame.Rect(GAME_WIDTH//2, HEIGHT-80, 60, 40)
#     return player, [], [], 0, MAX_LIVES

# # Star background
# stars = [(random.randint(0, GAME_WIDTH), random.randint(0, HEIGHT)) for _ in range(80)]

# # =========================
# # INITIAL STATE
# # =========================
# player, bullets, enemies, score, lives = reset_game()
# game_state = "MENU"
# shoot_cooldown = 0
# running = True

# # =========================
# # MAIN LOOP
# # =========================
# while running:
#     clock.tick(60)
#     screen.fill((5, 5, 20))

#     # ======== CAMERA ========
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb)

#     fingers = 0

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#             fingers = count_fingers(hand_landmarks)

#             # Highlight fingertip
#             tip = hand_landmarks.landmark[8]
#             h, w, _ = frame.shape
#             cx, cy = int(tip.x * w), int(tip.y * h)
#             cv2.circle(frame, (cx, cy), 15, (0,255,255), 3)

#             if game_state == "PLAYING":
#                 player.x = int(hand_landmarks.landmark[9].x * GAME_WIDTH)

#     # Convert camera
#     frame = cv2.resize(frame, (CAM_WIDTH, HEIGHT))
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = np.rot90(frame)
#     cam_surface = pygame.surfarray.make_surface(frame)

#     # ======== DRAW STARS ========
#     for i in range(len(stars)):
#         pygame.draw.circle(screen, (255,255,255), stars[i], 2)
#         stars[i] = (stars[i][0], stars[i][1] + 2)
#         if stars[i][1] > HEIGHT:
#             stars[i] = (random.randint(0, GAME_WIDTH), 0)

#     # =========================
#     # MENU STATE
#     # =========================
#     if game_state == "MENU":
#         title = big_font.render("GESTURE SPACE SHOOTER", True, (255,255,255))
#         instruction = font.render("Show 2 Fingers To Start", True, (0,255,255))

#         screen.blit(title, (GAME_WIDTH//2 - 250, HEIGHT//2 - 80))
#         screen.blit(instruction, (GAME_WIDTH//2 - 170, HEIGHT//2 - 20))

#         if fingers == 2:
#             player, bullets, enemies, score, lives = reset_game()
#             game_state = "PLAYING"

#     # =========================
#     # PLAYING STATE
#     # =========================
#     elif game_state == "PLAYING":

#         # Shoot
#         if fingers >= 4 and shoot_cooldown <= 0:
#             bullets.append(pygame.Rect(player.centerx-5, player.y, 10, 20))
#             shoot_cooldown = 15

#         # Bullets
#         for bullet in bullets:
#             bullet.y -= BULLET_SPEED
#             pygame.draw.rect(screen, (255,255,0), bullet)

#         bullets = [b for b in bullets if b.y > 0]

#         # Enemies
#         if random.randint(1, 30) == 1:
#             enemies.append(pygame.Rect(random.randint(0, GAME_WIDTH-40), -50, 40, 40))

#         for enemy in enemies:
#             enemy.y += ENEMY_SPEED
#             pygame.draw.rect(screen, (255,0,0), enemy)

#         # Collision
#         for enemy in enemies[:]:
#             for bullet in bullets[:]:
#                 if enemy.colliderect(bullet):
#                     enemies.remove(enemy)
#                     bullets.remove(bullet)
#                     score += 10
#                     break

#             if enemy.colliderect(player):
#                 enemies.remove(enemy)
#                 lives -= 1
#                 if lives <= 0:
#                     game_state = "MENU"

#         enemies = [e for e in enemies if e.y < HEIGHT]

#         # Draw Player
#         pygame.draw.rect(screen, (0,255,100), player)

#         # Health Bar
#         pygame.draw.rect(screen, (100,100,100), (10,10,200,20))
#         pygame.draw.rect(screen, (0,255,0), (10,10,200*(lives/MAX_LIVES),20))

#         score_text = font.render(f"Score: {score}", True, (255,255,255))
#         screen.blit(score_text, (10,40))

#         if shoot_cooldown > 0:
#             shoot_cooldown -= 1

#     # =========================
#     # DRAW CAMERA
#     # =========================
#     screen.blit(cam_surface, (GAME_WIDTH, 0))

#     pygame.display.update()

#     # Close only if window closed
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# cap.release()
# pygame.quit()
# cv2.destroyAllWindows()
# cap.release()
# pygame.quit()
# cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import pygame
import random
import numpy as np

# =========================
# CONFIG
# =========================
GAME_WIDTH = 800
CAM_WIDTH = 400
HEIGHT = 600
TOTAL_WIDTH = GAME_WIDTH + CAM_WIDTH

BULLET_SPEED = 10
ENEMY_SPEED = 5
MAX_LIVES = 2

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
    player = pygame.Rect(GAME_WIDTH//2, HEIGHT-80, 80, 60)
    return player, [], [], 0, MAX_LIVES

# =========================
# BACKGROUND STARS
# =========================
stars = [(random.randint(0, GAME_WIDTH), random.randint(0, HEIGHT)) for _ in range(80)]

# =========================
# INITIAL STATE
# =========================
player, bullets, enemies, score, lives = reset_game()
game_state = "MENU"
shoot_cooldown = 0
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

    # Clamp player inside screen
    player.x = max(0, min(player.x, GAME_WIDTH - 80))

    # Convert camera to pygame surface
    frame = cv2.resize(frame, (CAM_WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    cam_surface = pygame.surfarray.make_surface(frame)

    # ===== DRAW STARS =====
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
        instruction = font.render("Show 2 Fingers To Start", True, (0,255,255))

        screen.blit(title, (GAME_WIDTH//2 - 180, HEIGHT//2 - 80))
        screen.blit(instruction, (GAME_WIDTH//2 - 150, HEIGHT//2 - 20))

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

        # Enemies
        if random.randint(1, 30) == 1:
            enemies.append(pygame.Rect(random.randint(0, GAME_WIDTH-40), -50, 40, 40))

        for enemy in enemies:
            enemy.y += ENEMY_SPEED
            pygame.draw.rect(screen, (255,0,0), enemy)

        # Collision
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
                    game_state = "MENU"

        enemies = [e for e in enemies if e.y < HEIGHT]

        # Draw fighter plane
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

    # Only close if user clicks X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
pygame.quit()
cv2.destroyAllWindows()