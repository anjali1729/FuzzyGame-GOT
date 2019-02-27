import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyRules(object):


    def __init__(self):
        # initialize all rules
        #########################################################################################
        # SPEED
        #########################################################################################
        speed = ctrl.Antecedent(np.arange(0, 8, 1), 'speed_variations')
        fuzzy_speed = ctrl.Consequent(np.arange(0, 8, 1), 'fuzzy_speed_variations')

        speed['slow'] = fuzz.trapmf(speed.universe,[0, 1, 2, 3])
        speed['medium'] = fuzz.trapmf(speed.universe,[2, 3, 4, 5])
        speed['fast'] = fuzz.trapmf(speed.universe, [4,5,6,7])

        fuzzy_speed['slow'] = fuzz.trimf(speed.universe, [1, 1, 1])
        fuzzy_speed['medium'] = fuzz.trimf(speed.universe, [1, 1, 2])
        fuzzy_speed['fast'] = fuzz.trimf(speed.universe, [2, 2, 3])

        rule_fast_speed = ctrl.Rule(speed['fast'], fuzzy_speed['fast'])
        rule_medium_speed = ctrl.Rule(speed['medium'], fuzzy_speed['medium'])
        rule_slow_speed = ctrl.Rule(speed['slow'], fuzzy_speed['slow'])

        movement_ctrl_speed = ctrl.ControlSystem([rule_fast_speed, rule_medium_speed, rule_slow_speed])
        self.movement_score = ctrl.ControlSystemSimulation(movement_ctrl_speed)

        #########################################################################################
        # ATTACK
        #########################################################################################
        attack = ctrl.Antecedent(np.arange(0, 100, 1), 'attack_variations')
        fuzzy_attack = ctrl.Consequent(np.arange(0, 100, 1), 'fuzzy_attack_variations')

        attack['low'] = fuzz.trimf(attack.universe,[0, 15, 30])
        attack['medium'] = fuzz.trimf(attack.universe,[25, 40, 65])
        attack['high'] = fuzz.trimf(attack.universe, [60, 75, 100])

        fuzzy_attack['low'] = fuzz.trimf(attack.universe,[0, 15, 30])
        fuzzy_attack['medium'] = fuzz.trimf(attack.universe,[25, 40, 65])
        fuzzy_attack['high'] = fuzz.trimf(attack.universe, [60, 75, 100])

        rule_high_attack = ctrl.Rule(attack['high'], fuzzy_attack['high'])
        rule_medium_attack = ctrl.Rule(attack['medium'], fuzzy_attack['medium'])
        rule_low_attack = ctrl.Rule(attack['low'], fuzzy_attack['low'])

        movement_ctrl_attack = ctrl.ControlSystem([rule_high_attack, rule_medium_attack, rule_low_attack])
        self.attack_score = ctrl.ControlSystemSimulation(movement_ctrl_attack)

        #########################################################################################
        # ROAM OR STICK TOGETHER
        #########################################################################################
        roam = ctrl.Antecedent(np.arange(0, 10, 1), 'roam')
        roam['yes'] = fuzz.trimf(roam.universe, [0, 5, 7])
        roam['no'] = fuzz.trimf(roam.universe, [5, 7, 10])

        fuzzy_roam = ctrl.Consequent(np.arange(0, 10, 1), 'fuzzy_roam_variations')
        fuzzy_roam['yes'] = fuzz.trimf(fuzzy_roam.universe,[0, 5, 7])
        fuzzy_roam['no'] = fuzz.trimf(fuzzy_roam.universe,[5, 7, 10])

        rule_roam_yes = ctrl.Rule(roam['yes'], fuzzy_roam['yes'])
        rule_roam_no = ctrl.Rule(roam['no'], fuzzy_roam['no'])

        fuzzy_ctrl_roam = ctrl.ControlSystem([rule_roam_yes, rule_roam_no])
        self.roam_score = ctrl.ControlSystemSimulation(fuzzy_ctrl_roam)


        #########################################################################################
        # DECISION MAKING - WHETHER TO STAY, MOVE OR ATTACK
        #########################################################################################
        health = ctrl.Antecedent(np.arange(0, 300, 1), 'health')
        ogre_team = ctrl.Antecedent(np.arange(0, 49, 1), 'ogre_team')
        goblin_team = ctrl.Antecedent(np.arange(0, 25, 1), 'goblin_team')
        troll_team = ctrl.Antecedent(np.arange(0, 81, 1), 'troll_team')
        ogre_enemy_goblin = ctrl.Antecedent(np.arange(0, 49, 1), 'ogre_enemy_goblin')
        goblin_enemy_ogre = ctrl.Antecedent(np.arange(0, 25, 1), 'goblin_enemy_ogre')
        troll_enemy_goblin = ctrl.Antecedent(np.arange(0, 81, 1), 'troll_enemy_goblin')
        ogre_enemy_troll = ctrl.Antecedent(np.arange(0, 49, 1), 'ogre_enemy_troll')
        goblin_enemy_troll = ctrl.Antecedent(np.arange(0, 25, 1), 'goblin_enemy_troll')
        troll_enemy_ogre = ctrl.Antecedent(np.arange(0, 81, 1), 'troll_enemy_ogre')

        movement = ctrl.Consequent(np.arange(0, 101, 1), 'movement')

        movement['stay'] = fuzz.trapmf(movement.universe, [0, 10, 15, 20])
        movement['attack'] = fuzz.trapmf(movement.universe, [15, 40, 60, 70])
        movement['move'] = fuzz.trapmf(movement.universe, [60, 70, 90, 100])

        health['low'] = fuzz.trimf(health.universe, [0, 50, 120])
        health['medium'] = fuzz.trimf(health.universe, [100, 150, 200])
        health['high'] = fuzz.trimf(health.universe, [180, 200, 300])

        goblin_team['one'] = fuzz.trapmf(goblin_team.universe, [0, 0, 1, 2])
        goblin_team['small'] = fuzz.trapmf(goblin_team.universe, [1, 1, 2, 4])
        goblin_team['medium'] = fuzz.trapmf(goblin_team.universe, [3, 4, 5, 6])
        goblin_team['large'] = fuzz.trapmf(goblin_team.universe, [5, 6, 8, 10])

        ogre_team['one'] = fuzz.trapmf(ogre_team.universe, [0, 0, 1, 2])
        ogre_team['small'] = fuzz.trapmf(ogre_team.universe, [1, 1, 2, 4])
        ogre_team['medium'] = fuzz.trapmf(ogre_team.universe, [3, 4, 5, 6])
        ogre_team['large'] = fuzz.trapmf(ogre_team.universe, [5, 6, 8, 10])

        troll_team['one'] = fuzz.trapmf(troll_team.universe, [0, 0, 1, 2])
        troll_team['small'] = fuzz.trapmf(troll_team.universe, [1, 1, 2, 4])
        troll_team['medium'] = fuzz.trapmf(troll_team.universe, [3, 4, 5, 6])
        troll_team['large'] = fuzz.trapmf(troll_team.universe, [5, 6, 8, 10])

        ogre_enemy_goblin['one'] = fuzz.trapmf(ogre_enemy_goblin.universe, [0, 0, 1, 2])
        ogre_enemy_goblin['small'] = fuzz.trapmf(ogre_enemy_goblin.universe, [1, 1, 3, 5])
        ogre_enemy_goblin['medium'] = fuzz.trapmf(ogre_enemy_goblin.universe, [3, 5, 15, 20])
        ogre_enemy_goblin['large'] = fuzz.trapmf(ogre_enemy_goblin.universe, [15, 20, 48, 48])

        ogre_enemy_troll['one'] = fuzz.trapmf(ogre_enemy_troll.universe, [0, 0, 1, 2])
        ogre_enemy_troll['small'] = fuzz.trapmf(ogre_enemy_troll.universe, [1, 1, 2, 4])
        ogre_enemy_troll['medium'] = fuzz.trapmf(ogre_enemy_troll.universe, [2, 4, 10, 15])
        ogre_enemy_troll['large'] = fuzz.trapmf(ogre_enemy_troll.universe, [10, 15, 48, 48])

        goblin_enemy_ogre['one'] = fuzz.trapmf(goblin_enemy_ogre.universe, [0, 0, 1, 2])
        goblin_enemy_ogre['small'] = fuzz.trapmf(goblin_enemy_ogre.universe, [1, 1, 3, 5])
        goblin_enemy_ogre['medium'] = fuzz.trapmf(goblin_enemy_ogre.universe, [3, 5, 10, 15])
        goblin_enemy_ogre['large'] = fuzz.trapmf(goblin_enemy_ogre.universe, [10, 15, 24, 24])

        goblin_enemy_troll['one'] = fuzz.trapmf(goblin_enemy_troll.universe, [0, 0, 1, 2])
        goblin_enemy_troll['small'] = fuzz.trapmf(goblin_enemy_troll.universe, [1, 1, 2, 5])
        goblin_enemy_troll['medium'] = fuzz.trapmf(goblin_enemy_troll.universe, [2, 5, 10, 15])
        goblin_enemy_troll['large'] = fuzz.trapmf(goblin_enemy_troll.universe, [10, 15, 24, 24])

        troll_enemy_goblin['one'] = fuzz.trapmf(troll_enemy_goblin.universe, [0, 0, 1, 2])
        troll_enemy_goblin['small'] = fuzz.trapmf(troll_enemy_goblin.universe, [1, 1, 5, 10])
        troll_enemy_goblin['medium'] = fuzz.trapmf(troll_enemy_goblin.universe, [5, 10, 20, 25])
        troll_enemy_goblin['large'] = fuzz.trapmf(troll_enemy_goblin.universe, [20, 25, 80, 80])

        troll_enemy_ogre['one'] = fuzz.trapmf(troll_enemy_ogre.universe, [0, 0, 1, 2])
        troll_enemy_ogre['small'] = fuzz.trapmf(troll_enemy_ogre.universe, [1, 1, 2, 5])
        troll_enemy_ogre['medium'] = fuzz.trapmf(troll_enemy_ogre.universe, [2, 5, 10, 15])
        troll_enemy_ogre['large'] = fuzz.trapmf(troll_enemy_ogre.universe, [10, 15, 80, 80])

        rule5 = ctrl.Rule(goblin_team['one'] & goblin_enemy_ogre['one'], movement['attack'])
        rule6 = ctrl.Rule(goblin_team['one'] & goblin_enemy_ogre['small'], movement['move'])
        rule7 = ctrl.Rule(goblin_team['one'] & goblin_enemy_ogre['medium'], movement['move'])
        rule8 = ctrl.Rule(goblin_team['one'] & goblin_enemy_ogre['large'], movement['move'])

        rule9 = ctrl.Rule(goblin_team['small'] & goblin_enemy_ogre['one'], movement['attack'])
        rule10 = ctrl.Rule(goblin_team['small'] & goblin_enemy_ogre['small'], movement['attack'])
        rule11 = ctrl.Rule(goblin_team['small'] & goblin_enemy_ogre['medium'], movement['move'])
        rule12 = ctrl.Rule(goblin_team['small'] & goblin_enemy_ogre['large'], movement['move'])

        rule13 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_ogre['one'], movement['attack'])
        rule14 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_ogre['small'], movement['attack'])
        rule15 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_ogre['medium'], movement['move'])
        rule16 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_ogre['large'], movement['move'])

        rule17 = ctrl.Rule(goblin_team['large'] & goblin_enemy_ogre['one'], movement['attack'])
        rule18 = ctrl.Rule(goblin_team['large'] & goblin_enemy_ogre['small'], movement['attack'])
        rule19 = ctrl.Rule(goblin_team['large'] & goblin_enemy_ogre['medium'], movement['attack'])
        rule20 = ctrl.Rule(goblin_team['large'] & goblin_enemy_ogre['large'], movement['move'])

        rule21 = ctrl.Rule(goblin_team['one'] & goblin_enemy_troll['one'], movement['move'])
        rule22 = ctrl.Rule(goblin_team['one'] & goblin_enemy_troll['small'], movement['move'])
        rule23 = ctrl.Rule(goblin_team['one'] & goblin_enemy_troll['medium'], movement['move'])
        rule24 = ctrl.Rule(goblin_team['one'] & goblin_enemy_troll['large'], movement['move'])

        rule25 = ctrl.Rule(goblin_team['small'] & goblin_enemy_troll['one'], movement['attack'])
        rule26 = ctrl.Rule(goblin_team['small'] & goblin_enemy_troll['small'], movement['attack'])
        rule27 = ctrl.Rule(goblin_team['small'] & goblin_enemy_troll['medium'], movement['move'])
        rule28 = ctrl.Rule(goblin_team['small'] & goblin_enemy_troll['large'], movement['move'])

        rule29 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_troll['one'], movement['attack'])
        rule30 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_troll['small'], movement['attack'])
        rule31 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_troll['medium'], movement['attack'])
        rule32 = ctrl.Rule(goblin_team['medium'] & goblin_enemy_troll['large'], movement['move'])

        rule33 = ctrl.Rule(goblin_team['large'] & goblin_enemy_troll['one'], movement['attack'])
        rule34 = ctrl.Rule(goblin_team['large'] & goblin_enemy_troll['small'], movement['attack'])
        rule35 = ctrl.Rule(goblin_team['large'] & goblin_enemy_troll['medium'], movement['move'])
        rule36 = ctrl.Rule(goblin_team['large'] & goblin_enemy_troll['large'], movement['move'])

        rule1 = ctrl.Rule(ogre_team['one'] & ogre_enemy_goblin['one'], movement['attack'])
        rule2 = ctrl.Rule(ogre_team['one'] & ogre_enemy_goblin['small'], movement['attack'])
        rule3 = ctrl.Rule(ogre_team['one'] & ogre_enemy_goblin['medium'], movement['move'])
        rule4 = ctrl.Rule(ogre_team['one'] & ogre_enemy_goblin['large'], movement['move'])


        rule37 = ctrl.Rule(ogre_team['small'] & ogre_enemy_goblin['one'], movement['attack'])
        rule38 = ctrl.Rule(ogre_team['small'] & ogre_enemy_goblin['small'], movement['attack'])
        rule39 = ctrl.Rule(ogre_team['small'] & ogre_enemy_goblin['medium'], movement['attack'])
        rule40 = ctrl.Rule(ogre_team['small'] & ogre_enemy_goblin['large'], movement['move'])

        rule41 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_goblin['one'], movement['attack'])
        rule42 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_goblin['small'], movement['attack'])
        rule43 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_goblin['medium'], movement['attack'])
        rule44 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_goblin['large'], movement['attack'])

        rule45 = ctrl.Rule(ogre_team['large'] & ogre_enemy_goblin['one'], movement['attack'])
        rule46 = ctrl.Rule(ogre_team['large'] & ogre_enemy_goblin['small'], movement['attack'])
        rule47 = ctrl.Rule(ogre_team['large'] & ogre_enemy_goblin['medium'], movement['attack'])
        rule48 = ctrl.Rule(ogre_team['large'] & ogre_enemy_goblin['large'], movement['attack'])

        rule49 = ctrl.Rule(ogre_team['one'] & ogre_enemy_troll['one'], movement['attack'])
        rule50 = ctrl.Rule(ogre_team['one'] & ogre_enemy_troll['small'], movement['move'])
        rule51 = ctrl.Rule(ogre_team['one'] & ogre_enemy_troll['medium'], movement['move'])
        rule52 = ctrl.Rule(ogre_team['one'] & ogre_enemy_troll['large'], movement['move'])

        rule53 = ctrl.Rule(ogre_team['small'] & ogre_enemy_troll['one'], movement['attack'])
        rule54 = ctrl.Rule(ogre_team['small'] & ogre_enemy_troll['small'], movement['attack'])
        rule55 = ctrl.Rule(ogre_team['small'] & ogre_enemy_troll['medium'], movement['move'])
        rule56 = ctrl.Rule(ogre_team['small'] & ogre_enemy_troll['large'], movement['move'])

        rule57 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_troll['one'], movement['attack'])
        rule58 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_troll['small'], movement['attack'])
        rule59 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_troll['medium'], movement['move'])
        rule60 = ctrl.Rule(ogre_team['medium'] & ogre_enemy_troll['large'], movement['move'])

        rule61 = ctrl.Rule(ogre_team['large'] & ogre_enemy_troll['one'], movement['attack'])
        rule62 = ctrl.Rule(ogre_team['large'] & ogre_enemy_troll['small'], movement['attack'])
        rule63 = ctrl.Rule(ogre_team['large'] & ogre_enemy_troll['medium'], movement['attack'])
        rule64 = ctrl.Rule(ogre_team['large'] & ogre_enemy_troll['large'], movement['attack'])

        #########################################################################################

        rule65 = ctrl.Rule(troll_team['one'] & troll_enemy_goblin['one'], movement['attack'])
        rule66 = ctrl.Rule(troll_team['one'] & troll_enemy_goblin['small'], movement['attack'])
        rule67 = ctrl.Rule(troll_team['one'] & troll_enemy_goblin['medium'], movement['move'])
        rule68 = ctrl.Rule(troll_team['one'] & troll_enemy_goblin['large'], movement['move'])

        rule69 = ctrl.Rule(troll_team['small'] & troll_enemy_goblin['one'], movement['attack'])
        rule70 = ctrl.Rule(troll_team['small'] & troll_enemy_goblin['small'], movement['attack'])
        rule71 = ctrl.Rule(troll_team['small'] & troll_enemy_goblin['medium'], movement['move'])
        rule72 = ctrl.Rule(troll_team['small'] & troll_enemy_goblin['large'], movement['move'])

        rule73 = ctrl.Rule(troll_team['medium'] & troll_enemy_goblin['one'], movement['attack'])
        rule74 = ctrl.Rule(troll_team['medium'] & troll_enemy_goblin['small'], movement['attack'])
        rule75 = ctrl.Rule(troll_team['medium'] & troll_enemy_goblin['medium'], movement['attack'])
        rule76 = ctrl.Rule(troll_team['medium'] & troll_enemy_goblin['large'], movement['move'])

        rule77 = ctrl.Rule(troll_team['large'] & troll_enemy_goblin['one'], movement['attack'])
        rule78 = ctrl.Rule(troll_team['large'] & troll_enemy_goblin['small'], movement['attack'])
        rule79 = ctrl.Rule(troll_team['large'] & troll_enemy_goblin['medium'], movement['attack'])
        rule80 = ctrl.Rule(troll_team['large'] & troll_enemy_goblin['large'], movement['attack'])

        rule81 = ctrl.Rule(troll_team['one'] & troll_enemy_ogre['one'], movement['attack'])
        rule82 = ctrl.Rule(troll_team['one'] & troll_enemy_ogre['small'], movement['attack'])
        rule83 = ctrl.Rule(troll_team['one'] & troll_enemy_ogre['medium'], movement['move'])
        rule84 = ctrl.Rule(troll_team['one'] & troll_enemy_ogre['large'], movement['move'])

        rule85 = ctrl.Rule(troll_team['small'] & troll_enemy_ogre['one'], movement['attack'])
        rule86 = ctrl.Rule(troll_team['small'] & troll_enemy_ogre['small'], movement['attack'])
        rule87 = ctrl.Rule(troll_team['small'] & troll_enemy_ogre['medium'], movement['attack'])
        rule88 = ctrl.Rule(troll_team['small'] & troll_enemy_ogre['large'], movement['move'])

        rule89 = ctrl.Rule(troll_team['medium'] & troll_enemy_ogre['one'], movement['attack'])
        rule90 = ctrl.Rule(troll_team['medium'] & troll_enemy_ogre['small'], movement['attack'])
        rule91 = ctrl.Rule(troll_team['medium'] & troll_enemy_ogre['medium'], movement['attack'])
        rule92 = ctrl.Rule(troll_team['medium'] & troll_enemy_ogre['large'], movement['attack'])

        rule93 = ctrl.Rule(troll_team['large'] & troll_enemy_ogre['one'], movement['attack'])
        rule94 = ctrl.Rule(troll_team['large'] & troll_enemy_ogre['small'], movement['attack'])
        rule95 = ctrl.Rule(troll_team['large'] & troll_enemy_ogre['medium'], movement['attack'])
        rule96 = ctrl.Rule(troll_team['large'] & troll_enemy_ogre['large'], movement['attack'])

        #########################################################################################

        rule97 = ctrl.Rule(health['high'], movement['attack'])
        rule98 = ctrl.Rule(health['medium'], movement['attack'])
        rule99 = ctrl.Rule(health['low'], movement['move'])

        #########################################################################################

        movement_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12,
             rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23,
             rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule94, rule95, rule96,
             rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42,
             rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53,
             rule54, rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63, rule64,
             rule65, rule66, rule67, rule68, rule69, rule70, rule71, rule72, rule73, rule74, rule75,
             rule76, rule77, rule78, rule79, rule80, rule81, rule82, rule83, rule84, rule85, rule86,
             rule87, rule88, rule89, rule90, rule91, rule92, rule93, rule97,rule98,rule99])

        self.decision_score = ctrl.ControlSystemSimulation(movement_ctrl)

    def get_fuzzy_value_for_speed(self, speed_cmd):
        if speed_cmd == "fast":
            self.movement_score.input['speed_variations'] = 6

        elif speed_cmd == "medium":
            self.movement_score.input['speed_variations'] = 4

        elif speed_cmd == "slow":
            self.movement_score.input['speed_variations'] = 1

        self.movement_score.compute()
        return int(self.movement_score.output['fuzzy_speed_variations'])


    def get_fuzzy_value_for_attack(self, attack_cmd):
        if attack_cmd == "high":
            self.attack_score.input['attack_variations'] = random.randrange(60,100)

        elif attack_cmd == "medium":
            self.attack_score.input['attack_variations'] = random.randrange(30,50)

        elif attack_cmd == "low":
            self.attack_score.input['attack_variations'] = random.randrange(10,25)

        self.attack_score.compute()
        return int(self.attack_score.output['fuzzy_attack_variations'])


    def get_fuzzy_value_for_roaming(self, roam_count):
        self.roam_score.input(roam_count)
        self.roam_score.compute()
        return int(self.roam_score.output['fuzzy_roam_variations'])


    def make_fuzzy_decision(self, goblin_count, ogre_count, troll_count,team, health, display_input_output=True):
        self.decision_score.input['health'] = health
        self.decision_score.input['goblin_team'] = goblin_count
        self.decision_score.input['ogre_team'] = ogre_count
        self.decision_score.input['ogre_enemy_goblin'] = goblin_count
        self.decision_score.input['ogre_enemy_troll'] = troll_count
        self.decision_score.input['goblin_enemy_ogre'] = ogre_count
        self.decision_score.input['goblin_enemy_troll'] = troll_count
        self.decision_score.input['troll_team'] = troll_count
        self.decision_score.input['troll_enemy_goblin'] = goblin_count
        self.decision_score.input['troll_enemy_ogre'] = ogre_count

        self.decision_score.compute()
        decision = self.decision_score.output['movement']

        if display_input_output:
            print("***********************")
            print("FUZZY INPUTS:")
            print("health: " + str(health))
            print("goblin_team: " + str(goblin_count))
            print("ogre_team: " + str(ogre_count))
            print("troll_team: " + str(troll_count))
            print("defuzzified decision value: " + str(decision))
            print("***********************")

        # return either of 3 choices
        if decision <= 10:
            return "stay"
        elif decision >30 and decision <=70:
            return "attack"
        else:
            return "move"
