from hsp import HSP
from parser import parser
from predicate import hash_predicate


def main():
    print("salam")
    problem = parser("", "")
    hashed_init = state_to_set(problem.init_state)
    hashed_goals = state_to_set(problem.goal_state)
    hashed_ground_predicates = []
    for p in problem.all_ground_predicates:
        hashed_ground_predicates.append(hash_predicate(p))
    HSP([], hashed_init, hashed_goals, problem.all_ground_operators, hashed_ground_predicates)


def state_to_set(state_object):
    state_predicates = state_object.predicates
    state = set()
    for predicate in state_predicates:
        state.add(hash_predicate((predicate, predicate.params)))
    return state

if __name__ == '__main__':
        main()
