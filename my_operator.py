from predicate import get_num_of_params_by_predicate_name, Predicate
from predicate import hash_predicate


class Operator:
    instances = []

    def __init__(self, name, num_of_params, params_name):
        self.name = name
        self.params_name = params_name
        self.num_of_params = num_of_params
        self.preconds = []
        self.added_effects = []
        self.negative_effects = []
        Operator.instances.append(self)

    def add_precond(self, precond):
        self.preconds.append(precond)

    def add_added_effects(self, added_effect):
        self.added_effects.append(added_effect)

    def add_deleted_effects(self, negative_effect):
        self.negative_effects.append(negative_effect)

    def __str__(self):
        return self.name + " " + "has " + str(self.num_of_params) + " parameters"


def operators_parser(lines):
    single_operator_info = []
    for line in lines[1:]:
        if line == '':
            single_operator_parser(single_operator_info)
            single_operator_info = []
        else:
            single_operator_info.append(line)


def single_operator_parser(lines):
    if len(lines) == 0:
        return
    name = lines[0].strip()

    num_of_parameters = int(lines[1].split(':')[1])

    counter = 2
    operator_params = []
    for line in lines[counter : counter + num_of_parameters]:
        operator_params.append(line)
        counter += 1

    o = Operator(name, num_of_parameters, operator_params)

    num_of_preconds = int(lines[counter].split(':')[1])
    counter += 1
    num_of_retrieved_predicates = 0
    while num_of_retrieved_predicates < num_of_preconds:
        predicate_name = lines[counter].strip()
        counter += 1

        num_of_predicate_params = get_num_of_params_by_predicate_name(predicate_name)
        predicate_params = []
        for line in lines[counter : counter + num_of_predicate_params]:
            predicate_params.append(line)
            counter += 1
        p = Predicate(predicate_name, num_of_predicate_params, predicate_params)
        o.add_precond(p)
        num_of_retrieved_predicates += 1

    num_of_added_effects = int(lines[counter].split(":")[1])
    counter += 1

    num_of_retrieved_added_effects = 0

    while num_of_retrieved_added_effects < num_of_added_effects:
        predicate_name = lines[counter].strip()
        counter += 1

        num_of_predicate_params = get_num_of_params_by_predicate_name(predicate_name)
        predicate_params = []
        for line in lines[counter : counter + num_of_predicate_params]:
            predicate_params.append(line)
            counter += 1
        p = Predicate(predicate_name, num_of_predicate_params, predicate_params)
        o.add_added_effects(p)
        num_of_retrieved_added_effects += 1

    num_of_deleted_effects = int(lines[counter].split(":")[1])
    counter += 1

    num_of_retrieved_deleted_effects = 0
    while num_of_retrieved_deleted_effects < num_of_deleted_effects:
        predicate_name = lines[counter].strip()
        counter += 1

        num_of_predicate_params = get_num_of_params_by_predicate_name(predicate_name)
        predicate_params = []
        for line in lines[counter : counter + num_of_predicate_params]:
            predicate_params.append(line)
            counter += 1
        p = Predicate(predicate_name, num_of_predicate_params, predicate_params)
        o.add_deleted_effects(p)
        num_of_retrieved_deleted_effects += 1


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
        res.append((effect, eff_params))
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
        res.append((effect, eff_params))
    return res


def check_preconditions(U, op):
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
        if ground_precondition not in U.predicates:
            return []
        res.append(ground_precondition)
    return res

