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

    def set_preconds(self, preconds):
        self.preconds = preconds

    def add_precond(self, precond):
        self.preconds.append(precond)

    def set_added_effects(self, added_effects):
        self.added_effects = added_effects


    def set_negative_effects(self, negative_effects):
        self.negative_effects = negative_effects


def operators_parser(lines):
    single_operator_info = []
    for line in lines[1:]:
        if len(line) < 1:
            single_operator_parser(lines)
            single_operator_info = []
        else:
            single_operator_info.append(line)

def single_operator_parser(lines):
    name = lines[0]

    num_of_parameters = int(lines[1].split(':')[1])

    counter = 2
    params = []
    for line in lines[counter, counter + num_of_parameters]:
        params.append(line)
        counter += 1

    o = Operator(name, num_of_parameters)

    num_of_preconds = int(lines[1].split(':')[counter])
    counter += 1
    num_of_retrieved_predicates = 0
    while num_of_retrieved_predicates < num_of_preconds:
        predicate_name = lines[counter]
        counter += 1

        num_of_predicate_params = get_num_of_params_by_predicate_name(predicate_name)
        predicate_params = []
        for line in lines[counter, counter + num_of_predicate_params]:
            predicate_params.append(line)
            counter += 1
        p = Predicate(predicate_params, num_of_predicate_params, params)
        o.add_precond(p)
