from random import randrange
import pygame

from game.Skeleton import Skeleton

class Troll(Skeleton):

    def __init__(self, up_image, down_image, left_image, right_image, attack_image, army_x,army_y, global_min_x, global_min_y, global_max_x, global_max_y, idx,scan_range,max_charge,attack,speed):
        Skeleton.__init__(self, up_image, down_image, left_image, right_image, attack_image, army_x,army_y, global_min_x, global_min_y, global_max_x, global_max_y)
        self.attack = attack
        self.speed = speed
        self.type = "T"
        self.scan_range = scan_range
        self.unique_id = "T" + str(idx)
        self.max_charge = max_charge
        self.font = pygame.font.SysFont('Sans', 15)


    def fuzzy_move(self, FuzzyRules, grid, _display_surf, temp_bot_coord_dict,highlighter):
        try:
            # scan the stage
            goblin_count, ogre_count, troll_count = self.scan_stage(grid)
            self.attack_charge_full+=1
            motive = None

            if ogre_count == 0 and goblin_count == 0:
                decision = "move"
                motive = "explore"
            else:
                decision = FuzzyRules.make_fuzzy_decision(goblin_count, ogre_count, troll_count, self.type, self.health)
                if self.previous_decision == decision and decision is not "move":
                    decision = "move"
                self.previous_decision = decision
            if decision == "stay":
                #self.draw(_display_surf)
                pass

            elif decision == "attack":
                #print(self.unique_id + " SAYS ATTACK!!")
                self.attack_rate = FuzzyRules.get_fuzzy_value_for_attack(self.attack)
                # decide where to attack
                if self.gridx - 1 >= 0 and grid[self.gridx - 1][self.gridy] != self.type and grid[self.gridx - 1][self.gridy] != '0' and grid[self.gridx - 1][self.gridy] != 'M':
                    if str(self.gridx - 1) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        enemy_bot = temp_bot_coord_dict[str(self.gridx - 1) + ":" + str(self.gridy)]
                        grid,enemy_bot, temp_bot_coord_dict = self.update(grid, _display_surf, True, "left", enemy_bot, temp_bot_coord_dict)
                        temp_bot_coord_dict[str(self.gridx - 1) + ":" + str(self.gridy)] = enemy_bot
                elif self.gridx + 1 < len(grid[0]) and grid[self.gridx + 1][self.gridy] != self.type and grid[self.gridx + 1][self.gridy] != '0' and grid[self.gridx + 1][self.gridy] != 'M':
                    if str(self.gridx + 1) + ":" + str(self.gridy) in temp_bot_coord_dict:
                        enemy_bot = temp_bot_coord_dict[str(self.gridx + 1) + ":" + str(self.gridy)]
                        grid,enemy_bot, temp_bot_coord_dict = self.update(grid, _display_surf, True, "right", enemy_bot, temp_bot_coord_dict)
                        temp_bot_coord_dict[str(self.gridx + 1) + ":" + str(self.gridy)] = enemy_bot
                elif self.gridy + 1 < len(grid) and grid[self.gridx][self.gridy + 1] != self.type and grid[self.gridx][self.gridy + 1] != '0' and grid[self.gridx][self.gridy + 1] != 'M':
                    if str(self.gridx) + ":" + str(self.gridy + 1) in temp_bot_coord_dict:
                        enemy_bot = temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy + 1)]
                        grid,enemy_bot, temp_bot_coord_dict = self.update(grid, _display_surf, True, "down", enemy_bot, temp_bot_coord_dict)
                        temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy + 1)] = enemy_bot
                elif self.gridy - 1 >= 0 and grid[self.gridx][self.gridy - 1] != self.type and grid[self.gridx][self.gridy - 1] != '0' and grid[self.gridx][self.gridy - 1] != 'M':
                    if str(self.gridx) + ":" + str(self.gridy - 1) in temp_bot_coord_dict:
                        enemy_bot = temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy - 1)]
                        grid,enemy_bot, temp_bot_coord_dict = self.update(grid, _display_surf, True, "up", enemy_bot, temp_bot_coord_dict)
                        temp_bot_coord_dict[str(self.gridx) + ":" + str(self.gridy - 1)] = enemy_bot
                else:  # move towards enemy
                    motive = "towards"
                    decision = "move"

            if decision == "move":
                proximity, side,decision = self.get_status_of_enemy(grid, motive)

                # determine fuzzy speed step
                self.step = FuzzyRules.get_fuzzy_value_for_speed(self.speed)
                if side == "up":
                    self.moveUp()
                elif side == "left":
                    self.moveLeft()
                elif side == "right":
                    self.moveRight()
                elif side == "down":
                    self.moveDown()
                else:
                    random_decision = int(randrange(1, 5))
                    if random_decision == 1:
                        self.moveUp()
                    elif random_decision == 2:
                        self.moveLeft()
                    elif random_decision == 3:
                        self.moveRight()
                    elif random_decision == 4:
                        self.moveDown()

                grid, enemy_bot, temp_bot_coord_dict = self.update(grid, _display_surf, False, None, None, temp_bot_coord_dict)

            _display_surf.blit(self.return_image_sprite(),(self.x,self.y))
            if highlighter:
                step_path = int(self.scan_range/ 2)
                for i in range(-step_path, step_path + 1):
                    for j in range(-step_path, step_path + 1):
                        for highlighter_idx in range(self.sprite_width):
                            _display_surf.set_at(((self.x + int(self.sprite_width / 2)) + i * highlighter_idx,
                                                  (self.y + int(self.sprite_height / 2)) + j * highlighter_idx),
                                                 (255, 255, 255))

            self.text = self.font.render(decision, True, (0, 0, 0), (255, 255, 255))
            self.textrect = self.text.get_rect()
            self.textrect.centerx = self.x + int(self.sprite_width / 2)
            self.textrect.centery = self.y + 1
            #_display_surf.blit(text, textrect)

            return grid, temp_bot_coord_dict
        except Exception as e:
            #print("exception in troll:",e)
            return grid, temp_bot_coord_dict


    def get_status_of_enemy(self, grid, motive):
        proximity = 1
        side = "up"
        side_retry = 0
        if motive is not None and motive == "explore":
            # either make a random move or
            # group together and move in unison
            random_decision = int(randrange(1, 5))
            if random_decision == 1:
                return 1, "up",motive
            elif random_decision == 2:
                return 1, "left",motive
            elif random_decision == 3:
                return 1, "right",motive
            elif random_decision == 4:
                return 1, "down",motive
        while side is None and side_retry<=3:
            for proximity in range(int(self.scan_range/2)):
                side = self.find_others(grid, ["O", "G"], proximity + 1,side_retry)
                side_retry+=1
            if side is not None and motive is not None and motive == "towards":
                print(self.unique_id + " PROCLAIMS \"CASTING HIGH ENERGY MAGIC!!\"")
                motive = 'charge-in'
                return proximity + 1, side,motive
            elif side is not None and motive is None:  # run away in opposite direction!!
                motive = 'run-away'
                if side == "up":
                    return 1, "down",motive
                elif side == "down":
                    return 1, "up",motive
                elif side == "left":
                    return 1, "right",motive
                elif side == "right":
                    return 1, "left",motive

        return proximity, side, motive


    def find_others(self, grid, person_type, proximity, side_retry):
        count_list = [0,0,0,0]  # left, right, down, up
        for person in person_type:
            if self.gridx - proximity >= 0 and grid[self.gridx - proximity][self.gridy] == person:
                count_list[0]+=1
            elif self.gridx + proximity < len(grid[0]) and grid[self.gridx + proximity][self.gridy] == person:
                count_list[1]+=1
            elif self.gridy + proximity < len(grid) and grid[self.gridx][self.gridy + proximity] == person:
                count_list[2]+=1
            elif self.gridy + proximity >= 0 and grid[self.gridx][self.gridy - proximity] == person:
                count_list[3]+=1


        if side_retry < len(count_list):
            for i in range(side_retry):
                count_list.remove(max(count_list))

        max_others = count_list.index(max(count_list))
        if max(count_list) > 0:
            if max_others == 0:
                return "left"
            elif max_others == 1:
                return "right"
            elif max_others == 2:
                return "down"
            elif max_others == 3:
                return "up"
        else:
            return None