from my_operator import check_preconditions, get_added_effects, get_deleted_effects
from problem import Problem
import itertools


def main():
    print("salam")
    problem = Problem()
    HSP([], problem.init_state, problem.all_ground_operators, problem.all_ground_predicates)


def HSP(plan, state, goals, actions, predicates):
    if goals.issubset(state):
        return plan
    options = []
    for action in actions:
        if len(check_preconditions(state, action)) > 0:
            next_s = next_state(state, action)
            res = delta(next_s, predicates, actions)
            options.append((action, res, next_s))
    while len(options) > 0:
        action_index = select_action(options, goals)
        option = options.pop(action_index)
        partial_plan = []
        partial_plan.extend(plan)
        partial_plan.append(option[0])
        new_plan = HSP(partial_plan, option[2], goals, actions, predicates)
        if len(new_plan) > 0:
            return new_plan
    return []


def select_action(options, goals):
    min_index = 0
    min_value = max_pairs(goals, options[0][1])
    for i in range(1, len(options)):
        temp = max_pairs(goals, options[1])
        if min_value > temp:
            min_value = temp
            min_index = i
    return min_index


def next_state(state, action):
    added = get_added_effects(action)
    deleted = get_deleted_effects(action)
    state.union(added)
    return state.difference(deleted)


def delta(s, all_ground_predicates, all_ground_operators):
    print("delta")

    res = dict()
    for p in all_ground_predicates:
        for q in all_ground_predicates:
            res[hash_predicates(p, q)] = -1

    for p in s:
        for q in s:
            res[hash_predicates(p, q)] = 0

    U = set()
    U = U.union(s)
    no_change = False
    while no_change:
        no_change = True
        for op in all_ground_operators:
            pre_connds = check_preconditions(U, op)
            if len(pre_connds) > 0:  # Check if operation is applicable on U
                effects = get_added_effects(op)
                U = U.union(effects)
                for p in effects:
                    for q in U:
                        key = hash_predicates(p, q)
                        last_value = res[key]
                        new_value = max_pairs(pre_connds, res) + 1
                        if last_value > new_value:
                            res[key] = new_value
                            no_change = False
    return res


def max_pairs(goals, res):
    if len(goals) == 1:
        goals.append(goals[0])
    pairs = set(itertools.combinations(goals, 2))
    maximum = 0
    for pair in pairs:
        maximum = max(maximum, res[hash_predicates(pair[0], pair[1])])
    return maximum


def hash_predicate(p):
    raw_predicate = (p[0].name, p[1])
    return hash(raw_predicate)


def hash_predicates(p, q):
    return hash(frozenset([p, q]))


if __name__ == '__main__':
        main()
