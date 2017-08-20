import sys

from my_operator import check_preconditions, get_added_effects, get_deleted_effects
import itertools
from predicate import hash_predicates,hash_predicate


def HSP(plan, state, goals, actions, predicates):
    goals_predicates = set(goals.predicates.keys())
    state_predicates = set(state.predicates.keys())
    if goals_predicates.issubset(state_predicates):
        return plan
    options = []
    for action in actions:
        if len(check_preconditions(state, action)) > 0:
            next_s = next_state(state, action)
            res = delta(next_s, predicates, actions)
            options.append((action, res, next_s))
    while len(options) > 0:
        action_index, action_cost = select_action(options, goals)
        option = options.pop(action_index)
        print "action : " + str(option[0][0].name) + str(option[0][1]) + ", cost : " +\
              str(action_cost) + ", state : " +\
              "  " + " ".join(str(predicate) + " " for predicate in state.predicates.values())
        partial_plan = []
        partial_plan.extend(plan)
        partial_plan.append(option[0])
        new_plan = HSP(partial_plan, option[2], goals, actions, predicates)
        if len(new_plan) > 0:
            return new_plan
    return []


def select_action(options, goals):
    min_index = 0
    min_value = max_pairs(goals.predicates, options[0][1])
    for i in range(1, len(options)):
        temp = max_pairs(goals.predicates, options[i][1])
        if temp < min_value:
            min_value = temp
            min_index = i
    return min_index, min_value


def next_state(state, action):
    added = get_added_effects(action)
    deleted = get_deleted_effects(action)
    nex_state = state.copy()
    nex_state.add_predicates(added)
    nex_state.delete_predicates(deleted)
    return nex_state


def delta(s, all_ground_predicates, all_ground_operators):
    res = dict()
    for p in all_ground_predicates:
        for q in all_ground_predicates:
            res[hash_predicates(p, q)] = sys.maxint

    for p in s.predicates:
        for q in s.predicates:
            res[hash_predicates(p, q)] = 0

    U = s.copy()
    change = True
    while change:
        change = False
        for op in all_ground_operators:
            pre_conds = check_preconditions(U, op)
            if len(pre_conds) > 0:  # Check if operation is applicable on U
                effects = get_added_effects(op)
                U.add_predicates(effects)
                hash_effects = dict()
                for effect in effects:
                    hash_effects[hash_predicate(effect)] = effect
                for p in hash_effects:
                    for q in U.predicates:
                        key = hash_predicates(p, q)
                        last_value = res[key]
                        requirements = dict()
                        requirements.update(pre_conds)
                        if q in hash_effects:
                            new_value = max_pairs(requirements, res) + 1
                        else:
                            requirements[q] = U.predicates[q]
                            new_value = max_pairs(requirements, res) + 1
                        if last_value > new_value:
                            res[key] = new_value
                            change = True
    return res


def max_pairs(goals, res):
    pairs = set()
    if len(goals) == 1:
        pairs.add((goals.keys()[0], goals.keys()[0]))
    else:
        pairs = set(itertools.combinations(goals.keys(), 2))
    maximum = 0
    for pair in pairs:
        key = hash_predicates(pair[0], pair[1])
        maximum = max(maximum, res[key])
    return maximum
