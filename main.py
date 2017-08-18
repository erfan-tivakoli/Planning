from operator import Operator
from predicate import Predicate
import itertools


max_inputs = 3
objects = []
objects_combinations = []
for i in range(0,max_inputs+1):
    objects_combinations.append(itertools.combinations_with_replacement(objects, i))
# all_ground_predicates = []
# all_ground_operators = []


def main():
    print("salam")
    a = [1,2,3]
    b = set(itertools.combinations(a, 2))
    for x in b:
        print(x)
    all_ground_predicates = get_all_ground_predicates()
    all_ground_operators = get_all_ground_operators()


def HSP(plan, state=set(), goals=set(), actions=[], predicates=[]):
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
    pairs = set(itertools.combinations(goals, 2))
    maximum = 0
    for pair in pairs:
        maximum = max(maximum, res[hash_predicates(pair[0], pair[1])])
    return maximum


def get_added_effects(op):
    res = []
    raw_op = op[0]
    params_values = op[1]
    params = dict()
    for i in range(0, len(raw_op.params_name)):
        name = raw_op.params_name[i]
        params[name] = params_values[i]
    effects = raw_op.added_effects
    for effect in effects:
        eff_params_name = effect.params
        eff_params = []
        for i in range(0,eff_params_name):
            name = eff_params_name[i]
            eff_params.append(params[name])
        ground_effect = hash_predicate((effect, eff_params))
        res.append(ground_effect)
    return res


def get_deleted_effects(op):
    res = []
    raw_op = op[0]
    params_values = op[1]
    params = dict()
    for i in range(0, len(raw_op.params_name)):
        name = raw_op.params_name[i]
        params[name] = params_values[i]
    effects = raw_op.negative_effects
    for effect in effects:
        eff_params_name = effect.params
        eff_params = []
        for i in range(0,eff_params_name):
            name = eff_params_name[i]
            eff_params.append(params[name])
        ground_effect = hash_predicate((effect, eff_params))
        res.append(ground_effect)
    return res


def check_preconditions(u, op):
    res = []
    raw_op = op[0]
    params_values = op[1]
    params = dict()
    for i in range(0, len(raw_op.params_name)):
        name = raw_op.params_name[i]
        params[name] = params_values[i]
    preconds = raw_op.preconds
    for precond in preconds:
        pre_params_name = precond.params
        pre_params = []
        for i in range(0,pre_params_name):
            name = pre_params_name[i]
            pre_params.append(params[name])
        ground_precondition = hash_predicate((precond, pre_params))
        if ground_precondition not in u:
            return []
        res.append(ground_precondition)
    return True


def hash_predicate(p):
    return hash(p)


def hash_predicates(p, q):
    return hash(frozenset([p, q]))


# def find_predicate()

def get_all_ground_operators():
    ground_operators = []
    operators = Operator.instances
    for operator in operators:
        all_possible_params = objects_combinations[operator.num_of_params]
        for param in all_possible_params:
            ground_operators.append((operator, param))
    return ground_operators


def get_all_ground_predicates():
    ground_predicates = []
    predicates = Predicate.instances
    for predicate in predicates:
        all_possible_params = objects_combinations[predicate.num_of_params]
        for param in all_possible_params:
            ground_predicates.append((predicate, param))
    return ground_predicates


if __name__ == '__main__':
        main()