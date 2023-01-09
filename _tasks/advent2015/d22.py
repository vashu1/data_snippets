from collections import defaultdict
import dataclasses

# You start with 50 hit points and 500 mana points.
you = (50, 0, 0, 500)

boss = (58, 0, 9, 0)

'''
    Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
'''


def attack_damage(damage, armor):
    return 1 if damage <= armor else (damage - armor)

@dataclasses.dataclass
class Effect:
    name: str
    mana_cost: int
    duration: int
    damage: int = 0
    heal: int = 0
    poison: int = 0
    armor: int = 0
    add_mana: int = 0


effects_list = [
    Effect(name='Magic Missile', mana_cost=53, duration=1, damage=4),
    Effect(name='Drain', mana_cost=73, duration=1, damage=2, heal=2),
    Effect(name='Shield', mana_cost=113, duration=6, armor=7),
    Effect(name='Poinson', mana_cost=173, duration=6, poison=3),
    Effect(name='Recharge', mana_cost=229, duration=5, add_mana=101),
]
min_mana_cost = max([e.mana_cost for e in effects_list])
effect_names = list(sorted([e.name for e in effects_list]))

# What is the least amount of mana you can spend and still win the fight?
# (Do not include mana recharge effects as "spending" negative mana.)


def state_to_str(state):
    you, boss, _, effects = state
    es = []
    for name in effect_names:
        if name in effects:
            duration, _ = effects[name]
            es.append(f'{name}:{duration}')
    return f'{you} {boss} {",".join(es)}'

BIG_NUM = int(1e6)
best_mana_cost = BIG_NUM
step = 0
state = {step: (you, boss, 0, {})}
action = defaultdict(str)
memo = {}


def run(step):
    global state, effects_list, best_mana_cost
    print(step)
    state_str = state_to_str(state[step])
    if state_str in memo:
        return memo[state_str]
    (your_hit_points, your_damage, your_armor, your_mana), (boss_hit_points, boss_damage, boss_armor, boss_mana), mana_spent, effects = state[step]
    if mana_spent > best_mana_cost:
        return BIG_NUM
    if your_mana < min_mana_cost:
        return BIG_NUM  # If you cannot afford to cast any spell, you lose.
    step += 1
    # apply old effects and drop expired
    effects = dict(effects)
    for name in list(effects.keys()):
        duration, effect = effects[name]
        boss_hit_points -= effect.poison  # apply poison
        your_mana += effect.add_mana  # recharge
        if duration <= 1:
            your_armor -= effect.armor
            del effects[name]
        else:
            effects[name] = (duration - 1, effect)
    # lose or win?
    if boss_hit_points <= 0:
        if best_mana_cost < mana_spent:
            print('\n\n\n')
            for i in range(0, step):
                print(i, action[i])
        best_mana_cost = min(best_mana_cost, mana_spent)
        return mana_spent
    # bosses attack
    if step % 2 == 0:
        your_hit_points -= attack_damage(boss_damage, your_armor)
        if your_hit_points <= 0:
            return BIG_NUM
        state[step] = ((your_hit_points, your_damage, your_armor, your_mana), (boss_hit_points, boss_damage, boss_armor, boss_mana), mana_spent, effects)
        return run(step)
    # cast new spell
    you_win = False
    if step % 2 == 1:
        for effect in effects_list:
            effects2 = dict(effects)
            your_hit_points2, your_damage2, your_armor2, your_mana2 = your_hit_points, your_damage, your_armor, your_mana
            boss_hit_points2, boss_damage2, boss_armor2, boss_mana2 = boss_hit_points, boss_damage, boss_armor, boss_mana
            mana_spent2 = mana_spent
            if effect.name in effects:  # still in effect
                continue
            action[step] = effect.name
            effects2[effect.name] = (effect.duration, effect)
            mana_spent2 += effect.mana_cost
            your_mana2 -= effect.mana_cost
            boss_hit_points2 -= attack_damage(effect.damage, 0)
            your_hit_points2 -= effect.heal
            if your_hit_points2 <= 0:
                print('\n\n\n')
                for i in range(0, step):
                    print(i, action[i])
                best_mana_cost = min(best_mana_cost, your_mana2)
            elif boss_hit_points2 <= 0:
                you_win = True
            else:
                you2 = your_hit_points2, your_damage2, your_armor2, your_mana2
                boss2 = boss_hit_points2, boss_damage2, boss_armor2, boss_mana2
                state[step] = (you2, boss2, mana_spent2, effects2)
                if run(step):
                    you_win = True
    memo[state_str] = you_win
    return you_win

run(0)
print(best_mana_cost)

