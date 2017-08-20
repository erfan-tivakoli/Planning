from predicate import get_num_of_params_by_predicate_name, Predicate
from predicate import hash_predicate


class State:

    def __init__(self):
        self.predicates = dict()
        # State.instances.append(self)

    def add_predicate(self, predicate):
        key = hash_predicate((predicate, predicate.params))
        self.predicates[key] = predicate

    def add_predicates(self, add_list):
        for add_item in add_list:
            key = hash_predicate(add_item)
            new_predicate = add_item[0].copy()
            new_predicate.params = add_item[1]
            self.predicates[key] = new_predicate

    def delete_predicates(self, delete_list):
        for delete_item in delete_list:
            key = hash_predicate(delete_item)
            self.predicates.pop(key, None)

    def remove_predicate(self, removed_predicate):
        for predicate in self.predicates:
            if predicate == removed_predicate:
                self.predicates.remove(predicate)
                break

    # def hash_state(self):
    #     state_predicates = self.predicates
    #     state = set()
    #     for predicate in state_predicates:
    #         state.add(hash_predicate((predicate, predicate.params)))
    #     self.hashed_predicates = state
    #     return state

    def __str__(self):
        return "The state has: " + ','.join(str(predicate) for predicate in self.predicates)

    def copy(self):
        newone = State()
        newone.predicates.update(self.predicates)
        return newone


def state_parser(lines):
    counter = 1
    s = State()
    while True:
        if counter == len(lines):
            break
        predicate_name = lines[counter].strip().lower()
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
    return s
