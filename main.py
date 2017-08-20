from hsp import HSP
from parser import parser
from predicate import hash_predicate


def main():
    import itertools
    # a = itertools.combinations_with_replacement([1, 2, 3], 2)
    # for b in a:
    #     print b
    problem = parser("domain.txt", "sussman-anomaly.txt")
    hashed_ground_predicates = dict()
    for p in problem.all_ground_predicates:
        hashed_ground_predicates[hash_predicate(p)] = p
    # for key in problem.init_state.predicates:
    #     print str(key) + " " + str(problem.init_state.predicates[key])
    plan = HSP([], problem.init_state, problem.goal_state, problem.all_ground_operators, hashed_ground_predicates)
    print "~~~~~~~~~~~~~~~~~~~~~~~Plan is:~~~~~~~~~~~~~~~~~~~~~~~"
    print '\n'.join(str(plan.index(operator)) + ": (" + str(operator[0].name) + " " + ' '.join(p for p in operator[1]) + ")" for operator in plan)



def test():
    from predicate import Predicate
    for p in Predicate.instances:
        print p


def state_to_set(state_object):
    state_predicates = state_object.predicates
    state = set()
    for predicate in state_predicates:
        state.add(hash_predicate((predicate, predicate.params)))
    return state

if __name__ == '__main__':
        main()
