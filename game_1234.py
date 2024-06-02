import pygame
from random import randint
from pathlib import Path
from typing import Tuple
import time

# Ширина та висота вікна виведення в пікселях
WIDTH = 800
HEIGHT = 600

coin_countdown = 2500
coin_interval = 100
COIN_COUNT = 10

game_time = 60 * 1000 
start_time = pygame.time.get_ticks()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        player_image = str(Path.cwd() / "images" / "mario.png")
        self.original_surf = pygame.image.load(player_image).convert_alpha()
        self.surf = pygame.transform.scale(self.original_surf, (60, 60))
        self.rect = self.surf.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

        
    def update(self, pos: Tuple):
        self.rect.center = pos

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin, self).__init__()
        coin_image = str(Path.cwd() / "images" / "coin.png")
        self.original_surf = pygame.image.load(coin_image).convert_alpha()
        self.surf = pygame.transform.scale(self.original_surf, (50, 50))
        self.rect = self.surf.get_rect(
            center=(
                randint(10, WIDTH - 10),
                randint(10, HEIGHT - 10),
            )
        )


pygame.init()
screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

ADDCOIN = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCOIN, coin_countdown)

# Налаштувати coin_list
coin_list = pygame.sprite.Group()
score = 0

coin_pickup_sound = pygame.mixer.Sound(
    str(Path.cwd() / "sounds" / "coin_pickup.mp3")
)

game_over_sound = pygame.mixer.Sound(
    str(Path.cwd() / "sounds" / "game-over.mp3")
)

# Створення спрайту гравця
player = Player()
initial_mouse_pos = pygame.mouse.get_pos()
player.update(initial_mouse_pos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDCOIN:
            new_coin = Coin()
            coin_list.add(new_coin)

            # Швидкість
            if len(coin_list) < 3:
                coin_countdown -= coin_interval
            # Need to have some interval
            if coin_countdown < 100:
                coin_countdown = 100

            # Скидання інтервалу
            pygame.time.set_timer(ADDCOIN, 0)
            pygame.time.set_timer(ADDCOIN, coin_countdown)

    # Оновлення позиції гравця
    player.update(pygame.mouse.get_pos())

    # Зіткнення гравця з монетою - видалення монети
    coins_collected = pygame.sprite.spritecollide(
        sprite=player, group=coin_list, dokill=True
    )
    # Зіткнення з монеткою
    for coin in coins_collected:
        score += 10
        coin_pickup_sound.play()

    # Перевірка, чи минуло 1 хвилина
    if pygame.time.get_ticks() - start_time >= game_time:
        running = False

    if len(coin_list) >= COIN_COUNT:
        running = False

    # Рожевий фон
    screen.fill((163, 169, 255))

    # монети
    for coin in coin_list:
        screen.blit(coin.surf, coin.rect)

    # Гравець
    screen.blit(player.surf, player.rect)

    # Деталі
    score_font = pygame.font.SysFont("any_font", 36)
    score_block = score_font.render(f"Score: {score}", False, (0, 0, 0))
    screen.blit(score_block, (35, 80))

    coin_font = pygame.font.SysFont("any_font", 36)
    coin_block = coin_font.render(f"| Coin Max: {len(coin_list)} / 10", False, (0, 0, 0))
    screen.blit(coin_block, (215, 35))

    times_font = pygame.font.SysFont("any_font", 36)
    times_block = times_font.render(f"Times: {int((pygame.time.get_ticks() - start_time)/1000)} / {game_time/1000}", False, (0, 0, 0))
    screen.blit(times_block, (35, 35))

    pygame.display.flip()
    clock.tick(30)


pygame.mouse.set_visible(False)
game_over_sound.play()
time.sleep(5)
print(f"\n[ the end ]\n Coin -> {score}\n Time -> {int((pygame.time.get_ticks()))/1000} s.")
pygame.quit()
