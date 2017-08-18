class Object:
    instances = []

    def __init__(self, name):
        self.name = name
        Object.instances.append(self)

    def __str__(self):
        return "We have an object named " + self.name


def objects_parser(lines):
    for line in lines[1:]:
        o = Object(line.strip())
