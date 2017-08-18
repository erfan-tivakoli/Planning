import re

from my_operator import operators_parser, Operator
from object import objects_parser, Object
from predicate import predicates_parser, Predicate
from state import state_parser, State


def parse(file_path):
    with open(file_path, 'r') as f:

        content = f.read()
        parts = re.split('\n\n\n', content)

        for part in parts:
            lines = part.split('\n')
            header_line = lines[0]
            if header_line.__contains__("PREDICATES"):
                predicates_parser(lines)
            elif header_line.__contains__("OPERATORS"):
                operators_parser(lines)
            elif header_line.__contains__("OBJECTS"):
                objects_parser(lines)
            elif header_line.__contains__("INITIAL-STATE"):
                state_parser(lines)
            elif header_line.__contains__("GOALS"):
                state_parser(lines)



if __name__ == '__main__':
    parse('./../FinalProjectTools/blocks-world (simplified)/domain.txt')
    print("~~~~~~~~~~~~~~~Predicates~~~~~~~~~~~~~~~")
    for predicate in Predicate.instances:
        print(predicate)

    print("~~~~~~~~~~~~~~~Operators~~~~~~~~~~~~~~~")
    for operator in Operator.instances:
        print(operator)

    parse('./../FinalProjectTools/blocks-world (simplified)/large-a.txt')
    print("~~~~~~~~~~~~~~~Objects~~~~~~~~~~~~~~~")
    for object in Object.instances:
        print(object)

    print("~~~~~~~~~~~~~~~States~~~~~~~~~~~~~~~")
    for state in State.instances:
        print(state)



