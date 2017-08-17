from my_operator import operators_parser, Operator
from predicate import predicates_parser, Predicate


def parse(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        counter = 0
        num_of_predicates = int(lines[counter].split(":")[1])
        predicates_parser(lines[:num_of_predicates + 1])

        counter += num_of_predicates + 1

        counter += 2

        operators_parser(lines[counter:])


if __name__ == '__main__':
    parse('./../FinalProjectTools/blocks-world (simplified)/domain.txt')
    print("~~~~~~~~~~~~~~~Predicates~~~~~~~~~~~~~~~")
    for predicate in Predicate.instances:
        print(predicate)

    print("~~~~~~~~~~~~~~~Operators~~~~~~~~~~~~~~~")
    for operator in Operator.instances:
        print(operator)
