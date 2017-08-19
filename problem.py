from my_operator import Operator
import itertools


class Problem:
    def __init__(self, num_of_objects, objects, init_state, goal_state, predicates):
        self.num_of_objects = num_of_objects
        self.objects = objects
        self.init_state = init_state
        self.goal_state = goal_state
        objects_combinations = []
        max_inputs = 2

        for i in range(0, max_inputs + 1):
            objects_combinations.append(list(itertools.permutations(objects, i)))

        self.all_ground_predicates = get_all_ground_predicates(predicates, objects_combinations)
        self.all_ground_operators = get_all_ground_operators(objects_combinations)

    def set_ground_predicates(self, all_ground_predicates):
        self.all_ground_predicates = all_ground_predicates


def get_all_ground_operators(objects_combinations):
    ground_operators = []
    operators = Operator.instances
    for op in operators:
        all_possible_params = objects_combinations[op.num_of_params]
        for param in all_possible_params:
            ground_operators.append((op, param))
    return ground_operators


def get_all_ground_predicates(predicates, objects_combinations):
    ground_predicates = []
    for predicate in predicates:
        all_possible_params = objects_combinations[predicate.num_of_params]
        for param in all_possible_params:
            ground_predicates.append((predicate, param))
    return ground_predicates

