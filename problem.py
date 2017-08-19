from my_operator import Operator
import itertools
from itertools import tee

class Problem:
    def __init__(self, num_of_objects, objects, init_state, goal_state, predicates):
        self.num_of_objects = num_of_objects
        self.objects = objects
        self.init_state = init_state
        self.goal_state = goal_state
        objects_combinations = []
        copy_of_objects_combinations = []
        max_inputs = 2

        for i in range(0, max_inputs + 1):
            objects_combinations.append(itertools.combinations_with_replacement(objects, i))
        for i in range(0, max_inputs + 1):
            copy_of_objects_combinations.append(itertools.combinations_with_replacement(objects, i))

        self.all_ground_predicates = get_all_ground_predicates(predicates, objects_combinations)
        self.all_ground_operators = get_all_ground_operators(copy_of_objects_combinations)

    def set_ground_predicates(self, all_ground_predicates):
        self.all_ground_predicates = all_ground_predicates


def get_all_ground_operators(objects_combinations):
    ground_operators = []
    operators = Operator.instances
    for operator in operators:
        all_possible_params = objects_combinations[operator.num_of_params]
        for param in all_possible_params:
            ground_operators.append((operator, param))
    return ground_operators


def get_all_ground_predicates(predicates, objects_combinations):
    ground_predicates = []
    for predicate in predicates:
        all_possible_params = objects_combinations[predicate.num_of_params]
        for param in all_possible_params:
            ground_predicates.append((predicate, param))
    return ground_predicates

