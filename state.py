from predicate import get_num_of_params_by_predicate_name, Predicate


class State:
    instances = []

    def __init__(self):
        self.predicates = []
        State.instances.append(self)

    def add_predicate(self, predicate):
        self.predicates.append(predicate)

    def remove_predicate(self, removed_predicate):
        for predicate in self.predicates:
            if predicate == removed_predicate:
                self.predicates.remove(predicate)
                break

    def __str__(self):
        return "The state has: " + ','.join(str(predicate) for predicate in self.predicates)


def state_parser(lines):
    counter = 1
    s = State()
    while True:
        if counter == len(lines):
            break
        predicate_name = lines[counter].strip()
        if predicate_name == '':
            break
        num_of_params = get_num_of_params_by_predicate_name(predicate_name)

        counter += 1
        predicate_params = []
        for line in lines[counter:counter + num_of_params]:
            predicate_params.append(line.strip())
            counter += 1
        p = Predicate(predicate_name, num_of_params, predicate_params)
        s.add_predicate(p)
