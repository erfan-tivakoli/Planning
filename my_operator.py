from predicate import get_num_of_params_by_predicate_name, Predicate


class Operator:
    instances = []

    def __init__(self, name, num_of_params):
        self.name = name
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
        if line == '\n':
            single_operator_parser(single_operator_info)
            single_operator_info = []
        else:
            single_operator_info.append(line)


def single_operator_parser(lines):
    name = lines[0].strip()

    num_of_parameters = int(lines[1].split(':')[1])

    counter = 2
    operator_params = []
    for line in lines[counter : counter + num_of_parameters]:
        operator_params.append(line)
        counter += 1

    o = Operator(name, num_of_parameters)

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
