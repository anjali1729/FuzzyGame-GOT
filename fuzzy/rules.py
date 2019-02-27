import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# initialize all rules
#########################################################################################
# SPEED
#########################################################################################
speed = ctrl.Antecedent(np.arange(0, 8, 1), 'speed_variations')
fuzzy_speed = ctrl.Consequent(np.arange(0, 8, 1), 'fuzzy_speed_variations')


speed['slow'] = fuzz.trapmf(speed.universe,[0, 1, 2, 3])
speed['medium'] = fuzz.trapmf(speed.universe,[2, 3, 4, 5])
speed['fast'] = fuzz.trapmf(speed.universe, [4,5,6,7])

fuzzy_speed['slow'] = fuzz.trimf(speed.universe, [0, 1, 2])
fuzzy_speed['medium'] = fuzz.trimf(speed.universe, [1, 2, 3])
fuzzy_speed['fast'] = fuzz.trimf(speed.universe, [2, 3, 4])

rule_fast_speed = ctrl.Rule(speed['fast'], fuzzy_speed['fast'])
rule_medium_speed = ctrl.Rule(speed['medium'], fuzzy_speed['medium'])
rule_slow_speed = ctrl.Rule(speed['slow'], fuzzy_speed['slow'])

movement_ctrl_speed = ctrl.ControlSystem([rule_fast_speed, rule_medium_speed, rule_slow_speed])
movement_score = ctrl.ControlSystemSimulation(movement_ctrl_speed)

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
attack_score = ctrl.ControlSystemSimulation(movement_ctrl_attack)

#########################################################################################
# DECISION MAKING - WHETHER TO STAY, MOVE OR ATTACK
#########################################################################################
samurai_team = ctrl.Antecedent(np.arange(0, 49, 1), 'samurai_team')
ninja_team = ctrl.Antecedent(np.arange(0, 25, 1), 'ninja_team')
mage_team = ctrl.Antecedent(np.arange(0, 81, 1), 'mage_team')
samurai_enemy_ninja = ctrl.Antecedent(np.arange(0, 49, 1), 'samurai_enemy_ninja')
ninja_enemy_samurai = ctrl.Antecedent(np.arange(0, 25, 1), 'ninja_enemy_samurai')
mage_enemy_ninja = ctrl.Antecedent(np.arange(0, 81, 1), 'mage_enemy_ninja')
samurai_enemy_mage = ctrl.Antecedent(np.arange(0, 49, 1), 'samurai_enemy_mage')
ninja_enemy_mage = ctrl.Antecedent(np.arange(0, 25, 1), 'ninja_enemy_mage')
mage_enemy_samurai = ctrl.Antecedent(np.arange(0, 81, 1), 'mage_enemy_samurai')

movement = ctrl.Consequent(np.arange(0, 101, 1), 'movement')
# ninja - ninja
# samurai - Samurai
# mage - Mage
movement['stay'] = fuzz.trapmf(movement.universe, [0, 10, 15, 20])
movement['attack'] = fuzz.trapmf(movement.universe, [15, 40, 60, 70])
movement['move'] = fuzz.trapmf(movement.universe, [60, 70, 90, 100])


ninja_team['one'] = fuzz.trapmf(ninja_team.universe, [0, 0, 1, 2])
ninja_team['small'] = fuzz.trapmf(ninja_team.universe, [1, 1, 2, 4])
ninja_team['medium'] = fuzz.trapmf(ninja_team.universe, [3, 4, 5, 6])
ninja_team['large'] = fuzz.trapmf(ninja_team.universe, [5, 6, 8, 10])

samurai_team['one'] = fuzz.trapmf(samurai_team.universe, [0, 0, 1, 2])
samurai_team['small'] = fuzz.trapmf(samurai_team.universe, [1, 1, 2, 4])
samurai_team['medium'] = fuzz.trapmf(samurai_team.universe, [3, 4, 5, 6])
samurai_team['large'] = fuzz.trapmf(samurai_team.universe, [5, 6, 8, 10])

mage_team['one'] = fuzz.trapmf(mage_team.universe, [0, 0, 1, 2])
mage_team['small'] = fuzz.trapmf(mage_team.universe, [1, 1, 2, 4])
mage_team['medium'] = fuzz.trapmf(mage_team.universe, [3, 4, 5, 6])
mage_team['large'] = fuzz.trapmf(mage_team.universe, [5, 6, 8, 10])

samurai_enemy_ninja['one'] = fuzz.trapmf(samurai_enemy_ninja.universe, [0, 0, 1, 2])
samurai_enemy_ninja['small'] = fuzz.trapmf(samurai_enemy_ninja.universe, [1, 1, 3, 5])
samurai_enemy_ninja['medium'] = fuzz.trapmf(samurai_enemy_ninja.universe, [3, 5, 15, 20])
samurai_enemy_ninja['large'] = fuzz.trapmf(samurai_enemy_ninja.universe, [15, 20, 48, 48])

samurai_enemy_mage['one'] = fuzz.trapmf(samurai_enemy_mage.universe, [0, 0, 1, 2])
samurai_enemy_mage['small'] = fuzz.trapmf(samurai_enemy_mage.universe, [1, 1, 2, 4])
samurai_enemy_mage['medium'] = fuzz.trapmf(samurai_enemy_mage.universe, [2, 4, 10, 15])
samurai_enemy_mage['large'] = fuzz.trapmf(samurai_enemy_mage.universe, [10, 15, 48, 48])

ninja_enemy_samurai['one'] = fuzz.trapmf(ninja_enemy_samurai.universe, [0, 0, 1, 2])
ninja_enemy_samurai['small'] = fuzz.trapmf(ninja_enemy_samurai.universe, [1, 1, 3, 5])
ninja_enemy_samurai['medium'] = fuzz.trapmf(ninja_enemy_samurai.universe, [3, 5, 10, 15])
ninja_enemy_samurai['large'] = fuzz.trapmf(ninja_enemy_samurai.universe, [10, 15, 24, 24])

ninja_enemy_mage['one'] = fuzz.trapmf(ninja_enemy_mage.universe, [0, 0, 1, 2])
ninja_enemy_mage['small'] = fuzz.trapmf(ninja_enemy_mage.universe, [1, 1, 2, 5])
ninja_enemy_mage['medium'] = fuzz.trapmf(ninja_enemy_mage.universe, [2, 5, 10, 15])
ninja_enemy_mage['large'] = fuzz.trapmf(ninja_enemy_mage.universe, [10, 15, 24, 24])

mage_enemy_ninja['one'] = fuzz.trapmf(mage_enemy_ninja.universe, [0, 0, 1, 2])
mage_enemy_ninja['small'] = fuzz.trapmf(mage_enemy_ninja.universe, [1, 1, 5, 10])
mage_enemy_ninja['medium'] = fuzz.trapmf(mage_enemy_ninja.universe, [5, 10, 20, 25])
mage_enemy_ninja['large'] = fuzz.trapmf(mage_enemy_ninja.universe, [20, 25, 80, 80])

mage_enemy_samurai['one'] = fuzz.trapmf(mage_enemy_samurai.universe, [0, 0, 1, 2])
mage_enemy_samurai['small'] = fuzz.trapmf(mage_enemy_samurai.universe, [1, 1, 2, 5])
mage_enemy_samurai['medium'] = fuzz.trapmf(mage_enemy_samurai.universe, [2, 5, 10, 15])
mage_enemy_samurai['large'] = fuzz.trapmf(mage_enemy_samurai.universe, [10, 15, 80, 80])

rule5 = ctrl.Rule(ninja_team['one'] & ninja_enemy_samurai['one'], movement['attack'])
rule6 = ctrl.Rule(ninja_team['one'] & ninja_enemy_samurai['small'], movement['move'])
rule7 = ctrl.Rule(ninja_team['one'] & ninja_enemy_samurai['medium'], movement['move'])
rule8 = ctrl.Rule(ninja_team['one'] & ninja_enemy_samurai['large'], movement['move'])

rule9 = ctrl.Rule(ninja_team['small'] & ninja_enemy_samurai['one'], movement['attack'])
rule10 = ctrl.Rule(ninja_team['small'] & ninja_enemy_samurai['small'], movement['attack'])
rule11 = ctrl.Rule(ninja_team['small'] & ninja_enemy_samurai['medium'], movement['move'])
rule12 = ctrl.Rule(ninja_team['small'] & ninja_enemy_samurai['large'], movement['move'])

rule13 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_samurai['one'], movement['attack'])
rule14 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_samurai['small'], movement['attack'])
rule15 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_samurai['medium'], movement['move'])
rule16 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_samurai['large'], movement['move'])

rule17 = ctrl.Rule(ninja_team['large'] & ninja_enemy_samurai['one'], movement['attack'])
rule18 = ctrl.Rule(ninja_team['large'] & ninja_enemy_samurai['small'], movement['attack'])
rule19 = ctrl.Rule(ninja_team['large'] & ninja_enemy_samurai['medium'], movement['attack'])
rule20 = ctrl.Rule(ninja_team['large'] & ninja_enemy_samurai['large'], movement['move'])

rule21 = ctrl.Rule(ninja_team['one'] & ninja_enemy_mage['one'], movement['move'])
rule22 = ctrl.Rule(ninja_team['one'] & ninja_enemy_mage['small'], movement['move'])
rule23 = ctrl.Rule(ninja_team['one'] & ninja_enemy_mage['medium'], movement['move'])
rule24 = ctrl.Rule(ninja_team['one'] & ninja_enemy_mage['large'], movement['move'])

rule25 = ctrl.Rule(ninja_team['small'] & ninja_enemy_mage['one'], movement['attack'])
rule26 = ctrl.Rule(ninja_team['small'] & ninja_enemy_mage['small'], movement['attack'])
rule27 = ctrl.Rule(ninja_team['small'] & ninja_enemy_mage['medium'], movement['move'])
rule28 = ctrl.Rule(ninja_team['small'] & ninja_enemy_mage['large'], movement['move'])

rule29 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_mage['one'], movement['attack'])
rule30 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_mage['small'], movement['attack'])
rule31 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_mage['medium'], movement['attack'])
rule32 = ctrl.Rule(ninja_team['medium'] & ninja_enemy_mage['large'], movement['move'])

rule33 = ctrl.Rule(ninja_team['large'] & ninja_enemy_mage['one'], movement['attack'])
rule34 = ctrl.Rule(ninja_team['large'] & ninja_enemy_mage['small'], movement['attack'])
rule35 = ctrl.Rule(ninja_team['large'] & ninja_enemy_mage['medium'], movement['move'])
rule36 = ctrl.Rule(ninja_team['large'] & ninja_enemy_mage['large'], movement['move'])

rule1 = ctrl.Rule(samurai_team['one'] & samurai_enemy_ninja['one'], movement['attack'])
rule2 = ctrl.Rule(samurai_team['one'] & samurai_enemy_ninja['small'], movement['attack'])
rule3 = ctrl.Rule(samurai_team['one'] & samurai_enemy_ninja['medium'], movement['move'])
rule4 = ctrl.Rule(samurai_team['one'] & samurai_enemy_ninja['large'], movement['move'])


rule37 = ctrl.Rule(samurai_team['small'] & samurai_enemy_ninja['one'], movement['attack'])
rule38 = ctrl.Rule(samurai_team['small'] & samurai_enemy_ninja['small'], movement['attack'])
rule39 = ctrl.Rule(samurai_team['small'] & samurai_enemy_ninja['medium'], movement['attack'])
rule40 = ctrl.Rule(samurai_team['small'] & samurai_enemy_ninja['large'], movement['move'])

rule41 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_ninja['one'], movement['attack'])
rule42 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_ninja['small'], movement['attack'])
rule43 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_ninja['medium'], movement['attack'])
rule44 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_ninja['large'], movement['attack'])

rule45 = ctrl.Rule(samurai_team['large'] & samurai_enemy_ninja['one'], movement['attack'])
rule46 = ctrl.Rule(samurai_team['large'] & samurai_enemy_ninja['small'], movement['attack'])
rule47 = ctrl.Rule(samurai_team['large'] & samurai_enemy_ninja['medium'], movement['attack'])
rule48 = ctrl.Rule(samurai_team['large'] & samurai_enemy_ninja['large'], movement['attack'])

rule49 = ctrl.Rule(samurai_team['one'] & samurai_enemy_mage['one'], movement['attack'])
rule50 = ctrl.Rule(samurai_team['one'] & samurai_enemy_mage['small'], movement['move'])
rule51 = ctrl.Rule(samurai_team['one'] & samurai_enemy_mage['medium'], movement['move'])
rule52 = ctrl.Rule(samurai_team['one'] & samurai_enemy_mage['large'], movement['move'])

rule53 = ctrl.Rule(samurai_team['small'] & samurai_enemy_mage['one'], movement['attack'])
rule54 = ctrl.Rule(samurai_team['small'] & samurai_enemy_mage['small'], movement['attack'])
rule55 = ctrl.Rule(samurai_team['small'] & samurai_enemy_mage['medium'], movement['move'])
rule56 = ctrl.Rule(samurai_team['small'] & samurai_enemy_mage['large'], movement['move'])

rule57 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_mage['one'], movement['attack'])
rule58 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_mage['small'], movement['attack'])
rule59 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_mage['medium'], movement['move'])
rule60 = ctrl.Rule(samurai_team['medium'] & samurai_enemy_mage['large'], movement['move'])

rule61 = ctrl.Rule(samurai_team['large'] & samurai_enemy_mage['one'], movement['attack'])
rule62 = ctrl.Rule(samurai_team['large'] & samurai_enemy_mage['small'], movement['attack'])
rule63 = ctrl.Rule(samurai_team['large'] & samurai_enemy_mage['medium'], movement['attack'])
rule64 = ctrl.Rule(samurai_team['large'] & samurai_enemy_mage['large'], movement['attack'])

#########################################################################################

rule65 = ctrl.Rule(mage_team['one'] & mage_enemy_ninja['one'], movement['attack'])
rule66 = ctrl.Rule(mage_team['one'] & mage_enemy_ninja['small'], movement['attack'])
rule67 = ctrl.Rule(mage_team['one'] & mage_enemy_ninja['medium'], movement['move'])
rule68 = ctrl.Rule(mage_team['one'] & mage_enemy_ninja['large'], movement['move'])

rule69 = ctrl.Rule(mage_team['small'] & mage_enemy_ninja['one'], movement['attack'])
rule70 = ctrl.Rule(mage_team['small'] & mage_enemy_ninja['small'], movement['attack'])
rule71 = ctrl.Rule(mage_team['small'] & mage_enemy_ninja['medium'], movement['move'])
rule72 = ctrl.Rule(mage_team['small'] & mage_enemy_ninja['large'], movement['move'])

rule73 = ctrl.Rule(mage_team['medium'] & mage_enemy_ninja['one'], movement['attack'])
rule74 = ctrl.Rule(mage_team['medium'] & mage_enemy_ninja['small'], movement['attack'])
rule75 = ctrl.Rule(mage_team['medium'] & mage_enemy_ninja['medium'], movement['attack'])
rule76 = ctrl.Rule(mage_team['medium'] & mage_enemy_ninja['large'], movement['move'])

rule77 = ctrl.Rule(mage_team['large'] & mage_enemy_ninja['one'], movement['attack'])
rule78 = ctrl.Rule(mage_team['large'] & mage_enemy_ninja['small'], movement['attack'])
rule79 = ctrl.Rule(mage_team['large'] & mage_enemy_ninja['medium'], movement['attack'])
rule80 = ctrl.Rule(mage_team['large'] & mage_enemy_ninja['large'], movement['attack'])

rule81 = ctrl.Rule(mage_team['one'] & mage_enemy_samurai['one'], movement['attack'])
rule82 = ctrl.Rule(mage_team['one'] & mage_enemy_samurai['small'], movement['attack'])
rule83 = ctrl.Rule(mage_team['one'] & mage_enemy_samurai['medium'], movement['move'])
rule84 = ctrl.Rule(mage_team['one'] & mage_enemy_samurai['large'], movement['move'])

rule85 = ctrl.Rule(mage_team['small'] & mage_enemy_samurai['one'], movement['attack'])
rule86 = ctrl.Rule(mage_team['small'] & mage_enemy_samurai['small'], movement['attack'])
rule87 = ctrl.Rule(mage_team['small'] & mage_enemy_samurai['medium'], movement['attack'])
rule88 = ctrl.Rule(mage_team['small'] & mage_enemy_samurai['large'], movement['move'])

rule89 = ctrl.Rule(mage_team['medium'] & mage_enemy_samurai['one'], movement['attack'])
rule90 = ctrl.Rule(mage_team['medium'] & mage_enemy_samurai['small'], movement['attack'])
rule91 = ctrl.Rule(mage_team['medium'] & mage_enemy_samurai['medium'], movement['attack'])
rule92 = ctrl.Rule(mage_team['medium'] & mage_enemy_samurai['large'], movement['attack'])

rule93 = ctrl.Rule(mage_team['large'] & mage_enemy_samurai['one'], movement['attack'])
rule94 = ctrl.Rule(mage_team['large'] & mage_enemy_samurai['small'], movement['attack'])
rule95 = ctrl.Rule(mage_team['large'] & mage_enemy_samurai['medium'], movement['attack'])
rule96 = ctrl.Rule(mage_team['large'] & mage_enemy_samurai['large'], movement['attack'])

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
     rule87, rule88, rule89, rule90, rule91, rule92, rule93])

#decision_score = ctrl.ControlSystemSimulation(movement_ctrl)

movement_score = ctrl.ControlSystemSimulation(movement_ctrl)

movement_score.input['samurai_team'] = 1
movement_score.input['ninja_team'] = 3
movement_score.input['mage_team'] = 0
movement_score.input['ninja_team'] = 3
movement_score.input['mage_enemy_ninja'] = 3
movement_score.input['samurai_enemy_ninja'] = 3
movement_score.input['ninja_enemy_samurai'] = 1
movement_score.input['mage_enemy_samurai'] = 3
movement_score.input['samurai_enemy_mage'] = 3
movement_score.input['ninja_enemy_mage'] = 1

movement_score.compute()

print(movement_score.output['movement'])

samurai_team.view(sim=movement_score)
ninja_team.view(sim=movement_score)
mage_team.view(sim=movement_score)
samurai_enemy_ninja.view(sim=movement_score)
samurai_enemy_mage.view(sim=movement_score)
mage_enemy_samurai.view(sim=movement_score)
mage_enemy_ninja.view(sim=movement_score)
ninja_enemy_samurai.view(sim=movement_score)
ninja_enemy_mage.view(sim=movement_score)
movement.view(sim=movement_score)
speed.view(sim=movement_score)
fuzzy_speed.view(sim=movement_score)
attack.view(sim=movement_score)
fuzzy_attack.view(sim=movement_score)


