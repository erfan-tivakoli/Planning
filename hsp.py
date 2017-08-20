import sys

from my_operator import check_preconditions, get_added_effects, get_deleted_effects
import itertools
from predicate import hash_predicates, hash_predicate


def HSP(plan, state, goals, actions, predicates):
    goals_predicates = set(goals.predicates.keys())
    state_predicates = set(state.predicates.keys())
    if goals_predicates.issubset(state_predicates):
        return plan
    options = []
    visited_states = []
    for action in actions:
        if len(check_preconditions(state, action)) > 0:
            next_s = next_state(state, action)
            if have_visited_before(visited_states, next_s):
                continue
            res = delta(next_s, predicates, actions)
            options.append((action, res, next_s))
    while len(options) > 0:
        action_index = select_action(options, goals)
        option = options.pop(action_index)
        partial_plan = []
        partial_plan.extend(plan)
        partial_plan.append(option[0])

        next_s = next_state(state, option[0])
        visited_states.append(next_s)

        new_plan = HSP(partial_plan, option[2], goals, actions, predicates)
        if len(new_plan) > 0:
            return new_plan
    return []


def have_visited_before(visited_states, new_state):
    for visited_state in visited_states:
        if new_state == visited_state:
            return True
    return False


def select_action(options, goals):
    min_index = 0
    min_value = max_pairs(goals.predicates, options[0][1])
    for i in range(1, len(options)):
        temp = max_pairs(goals.predicates, options[i][1])
        if min_value > temp:
            min_value = temp
            min_index = i
    return min_index


def next_state(state, action):
    added = get_added_effects(action)
    deleted = get_deleted_effects(action)
    nex_state = state.copy()
    nex_state.add_predicates(added)
    nex_state.delete_predicates(deleted)
    return nex_state


def delta(s, all_ground_predicates, all_ground_operators):
    print("delta")

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
                for p in effects:
                    for q in U.predicates:
                        key = hash_predicates(hash_predicate(p), q)
                        last_value = res[key]
                        new_value = max_pairs(pre_conds, res) + 1
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
