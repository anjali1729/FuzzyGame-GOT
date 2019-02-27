from random import randrange
import pygame

class Skeleton:
    x = 0
    y = 0
    direction = -1
    step = 1
    image = None
    up_image = down_image = left_image = right_image = None
    attack_image = None
    health = 0
    attack = None
    attack_rate = 0
    attack_charge_full = 0
    speed = None
    _image_surf = None
    _attack_surf = None
    sprite_width = 60
    sprite_height = 60
    type = None
    COLON = ":"
    scan_range = None
    dead = False
    unique_id = None
    max_charge = 0
    text = None
    textrect = None
    previous_decision = 'move'

    def __init__(self, up_image, down_image, left_image, right_image, attack_image, army_x, army_y, global_min_x, global_min_y, global_max_x, global_max_y):
        self.health = 300
        # formation based on army coordinates
        self.global_min_x, self.global_min_y, self.global_max_x, self.global_max_y = global_min_x, global_min_y, global_max_x, global_max_y
        self.up_image = up_image
        self.down_image = down_image
        self.left_image = left_image
        self.right_image = right_image
        self.attack_image = attack_image
        img_up = pygame.image.load(self.up_image)   # sprite
        img_up = pygame.transform.scale(img_up, (60, 60))
        img_down = pygame.image.load(self.down_image)   # sprite
        img_left = pygame.image.load(self.left_image)   # sprite
        img_right = pygame.image.load(self.right_image)   # sprite
        self.sprite_width = img_up.get_width()
        self.sprite_height = img_up.get_height()
        self.gridy = army_y
        self.gridx = army_x
        self.x = army_x * self.sprite_width
        self.y = army_y * self.sprite_height
        self.font = pygame.font.SysFont('Sans', 15)
        self.text = self.font.render('stay', True, (255, 255, 255), (255, 255, 255))
        self.textrect = self.text.get_rect()

    def update(self, grid, display_surf, to_attack, direction, enemy_bot, temp_bot_coord_dict):
        self.attack_charge_full += 1
        if to_attack and self.attack_charge_full >= self.max_charge:
            enemy_bot = self.attack_enemy(display_surf, direction, enemy_bot, temp_bot_coord_dict)
            if enemy_bot.dead:
                if str(enemy_bot.gridx) + ":" + str(enemy_bot.gridy) in temp_bot_coord_dict:
                    #temp_bot_coord_dict.pop(str(enemy_bot.gridx) + ":" + str(enemy_bot.gridy), None)
                    grid[enemy_bot.gridx][enemy_bot.gridy] = '0'
        else:
            # update position
            if self.direction == 0 and (self.gridx + self.step) < self.global_max_x:
                if grid[(self.gridx + self.step)][self.gridy] == '0':
                    grid[(self.gridx)][self.gridy] = '0'
                    self.x = self.x + self.step * self.sprite_width
                    if str(self.gridx) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        temp_bot_coord_dict.pop(str(self.gridx) + ":" + str(self.gridy), None)
                    self.gridx += self.step
                    grid[(self.gridx)][self.gridy] = self.type
                    temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy)] = self

            if self.direction == 1 and (self.gridx - self.step) > self.global_min_x:
                if grid[(self.gridx - self.step)][self.gridy] == '0':
                    grid[(self.gridx)][self.gridy] = '0'
                    self.x = self.x - self.step * self.sprite_width
                    if str(self.gridx) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        temp_bot_coord_dict.pop(str(self.gridx) + ":" + str(self.gridy), None)
                    self.gridx -= self.step
                    grid[(self.gridx)][self.gridy] = self.type
                    temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy)] = self

            if self.direction == 2 and (self.gridy - self.step) > self.global_min_y:
                if grid[(self.gridx)][self.gridy - self.step] == '0':
                    grid[(self.gridx)][self.gridy] = '0'
                    self.y = self.y - self.step * self.sprite_height
                    if str(self.gridx) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        temp_bot_coord_dict.pop(str(self.gridx) + ":" + str(self.gridy), None)
                    self.gridy -= self.step
                    grid[(self.gridx)][self.gridy] = self.type
                    temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy)] = self

            if self.direction == 3 and (self.gridy + self.step) < self.global_max_y:
                if grid[(self.gridx)][self.gridy + self.step] == '0':
                    grid[(self.gridx)][self.gridy] = '0'
                    self.y = self.y + self.step * self.sprite_height
                    if str(self.gridx) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        temp_bot_coord_dict.pop(str(self.gridx) + ":" + str(self.gridy), None)
                    self.gridy += self.step
                    grid[(self.gridx)][self.gridy] = self.type
                    temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy)] = self

            else:
                if self.speed == "fast":
                    self.speed = "medium"
                elif self.speed == "medium":
                    self.speed = "slow"
                elif self.speed == "slow":
                    self.speed = "medium"
                text = self.font.render("stay", True, (0, 0, 0), (255, 255, 255))
                textrect = text.get_rect()
                textrect.centerx = self.x + int(self.sprite_width / 2)
                textrect.centery = self.y
                display_surf.blit(text, textrect)

        #self.draw(display_surf)
        return grid, enemy_bot, temp_bot_coord_dict


    def moveRight(self):
        self.direction = 0
        self.image = self.right_image
        self._image_surf = self._right_image_surf

    def moveLeft(self):
        self.direction = 1
        self.image = self.left_image
        self._image_surf = self._left_image_surf

    def moveUp(self):
        self.direction = 2
        self.image = self.up_image
        self._image_surf = self._up_image_surf

    def moveDown(self):
        self.direction = 3
        self.image = self.down_image
        self._image_surf = self._down_image_surf

    def create_avatar(self):
        self._up_image_surf = pygame.transform.scale(pygame.image.load(self.up_image), (self.sprite_width, self.sprite_height)).convert()
        self._down_image_surf = pygame.transform.scale(pygame.image.load(self.down_image), (self.sprite_width, self.sprite_height)).convert()
        self._left_image_surf = pygame.transform.scale(pygame.image.load(self.left_image), (self.sprite_width, self.sprite_height)).convert()
        self._right_image_surf = pygame.transform.scale(pygame.image.load(self.right_image), (self.sprite_width, self.sprite_height)).convert()

        attack_image = pygame.image.load(self.attack_image)
        #alpha = 128
        #attack_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self._attack_surf = pygame.transform.scale(attack_image, (self.sprite_width, self.sprite_height)).convert()
        self._image_surf = self._down_image_surf

    def draw(self, surface):
        surface.blit(self._image_surf, (self.x, self.y))

    def draw_decision(self, surface):
        surface.blit(self.text, self.textrect)

    def sense_range(self, rang, grid):
        step_path = int(rang/2)
        goblin_count = 0
        ogre_count = 0
        troll_count = 0

        for i in range(-step_path, step_path):
            for j in range(-step_path, step_path):
                if i >= 0 and self.gridx + i < len(grid) and j >=0 and self.gridy + j < len(grid[0]):
                    if grid[self.gridx + i][self.gridy + j] == 'G':
                        goblin_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'O':
                        ogre_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'T':
                        troll_count+=1

                elif i >=0 and self.gridx + i < len(grid) and j<0 and self.gridy + j >= 0:
                    if grid[self.gridx + i][self.gridy + j] == 'G':
                        goblin_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'O':
                        ogre_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'T':
                        troll_count+=1

                elif i<0 and self.gridx + i >= 0 and j>=0 and self.gridy + j < len(grid[0]):
                    if grid[self.gridx + i][self.gridy + j] == 'G':
                        goblin_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'O':
                        ogre_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'T':
                        troll_count+=1

                elif i<0 and self.gridx - i >= 0 and j<0 and self.gridy +j >= 0:
                    if grid[self.gridx + i][self.gridy + j] == 'G':
                        goblin_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'O':
                        ogre_count+=1
                    elif grid[self.gridx + i][self.gridy + j] == 'T':
                        troll_count+=1
        return goblin_count, ogre_count, troll_count


    def attack_enemy(self, surface, direction, enemy_bot, temp_bot_coord_dict):
        self.attack_charge_full = 0
        if direction == "up":
            surface.blit(self._attack_surf, (self.x, self.y - 1 * self.sprite_height))
            enemy_bot.health -= self.attack_rate
            print(self.unique_id + " ATTACKS " + enemy_bot.unique_id + " WITH A FORCE OF " + str(self.attack_rate) + " LEAVING ENEMY HEART AT " + str(enemy_bot.health))
        elif direction == "down":
            surface.blit(self._attack_surf, (self.x, self.y + 1 * self.sprite_height))
            enemy_bot.health -= self.attack_rate
            print(self.unique_id + " ATTACKS " + enemy_bot.unique_id + " WITH A FORCE OF " + str(self.attack_rate) + " LEAVING ENEMY HEART AT " + str(enemy_bot.health))
        elif direction == "left":
            surface.blit(self._attack_surf, (self.x - 1 * self.sprite_width, self.y))
            enemy_bot.health -= self.attack_rate
            print(self.unique_id + " ATTACKS " + enemy_bot.unique_id + " WITH A FORCE OF " + str(self.attack_rate) + " LEAVING ENEMY HEART AT " + str(enemy_bot.health))
        elif direction == "right":
            surface.blit(self._attack_surf, (self.x + 1 * self.sprite_width, self.y))
            enemy_bot.health -= self.attack_rate
            print(self.unique_id + " ATTACKS " + enemy_bot.unique_id + " WITH A FORCE OF " + str(self.attack_rate) + " LEAVING ENEMY HEART AT " + str(enemy_bot.health))

        if enemy_bot.health <= 0:
            enemy_bot.is_dead()
            print(enemy_bot.unique_id + " HAS DIED!")

        self.draw(surface)

        return enemy_bot

    def return_image_sprite(self):
        return self._image_surf

    def is_dead(self):
        self.dead = True

    def scan_stage(self, grid, print_range=False):
        goblin_count, ogre_count, troll_count = self.sense_range(self.scan_range,grid)
        if print_range:
            print("*******" + self.unique_id + "*********")
            print("Ninja Count: " + str(goblin_count))
            print("Samurai Count: " + str(ogre_count))
            print("Mage Count: " + str(troll_count))
            print("****************")
        return goblin_count, ogre_count, troll_count
