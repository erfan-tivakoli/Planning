import re

from my_operator import operators_parser, Operator
from object import objects_parser, Object
from predicate import predicates_parser, Predicate
from state import state_parser, State
from problem import Problem


def parse(file_path, all_predicates=None):
    with open(file_path, 'r') as f:

        content = f.read()
        parts = re.split('\n\r\n\r\n', content)
        is_problem = False
        for part in parts:
            raw_lines = part.split('\n')
            lines = []
            for raw_line in raw_lines:
                lines.append(raw_line.lower().strip("\n \t \r"))
            header_line = raw_lines[0]
            if header_line.__contains__("PREDICATES"):
                all_predicates = predicates_parser(lines)
            elif header_line.__contains__("OPERATORS"):
                operators_parser(lines)
            elif header_line.__contains__("OBJECTS"):
                is_problem = True
                objects_parser(lines)
            elif header_line.__contains__("INITIAL-STATE"):
                init_state = state_parser(lines)
            elif header_line.__contains__("GOALS"):
                goal_state = state_parser(lines)
        objects = []
        for ob in Object.instances:
            objects.append(ob.name)
        if is_problem:
            return Problem(len(objects), objects, init_state, goal_state, all_predicates)
        else:
            return all_predicates


def parser(domain_path, problem_path):
    all_predicates = parse('./../FinalProjectTools/blocks-world (simplified)/' + domain_path)

    problem = parse('./../FinalProjectTools/blocks-world (simplified)/' + problem_path, all_predicates)
    return problem
