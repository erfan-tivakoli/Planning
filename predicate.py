
class Predicate:
    instances = []

    def __init__(self, name, num_of_params):
        self.name = name
        self.num_of_params = num_of_params
        self.params = [None] * self.num_of_params
        Predicate.instances.append(self)


def predicates_parser(lines):
    for line in lines[1:]:
        single_predicate_parser(line)


def single_predicate_parser(line):
    name, num_of_params = line.split(':')