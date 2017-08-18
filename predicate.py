class Predicate:
    instances = []

    def __init__(self, name, num_of_params, params=None):
        self.name = name
        self.num_of_params = num_of_params
        self.params = params
        Predicate.instances.append(self)

    def __str__(self):
        return self.name + " has " + str(self.num_of_params) + " parameters"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.name == other.name and self.params == other.params:
                return True
        return False


def predicates_parser(lines):
    for line in lines[1:]:
        single_predicate_parser(line)


def single_predicate_parser(line):
    name, num_of_params = line.split(':')
    p = Predicate(name, int(num_of_params))


def get_num_of_params_by_predicate_name(name):
    name = name.lower().strip()
    for predicate in Predicate.instances:
        if predicate.name == name:
            return predicate.num_of_params
    return None

