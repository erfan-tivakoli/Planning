class Operator:
    instances = []

    def __init__(self, name, num_of_params):
        self.name = name
        self.num_of_params = num_of_params
        self.preconds = None
        self.added_effects = None
        self.negative_effects = None
        Operator.instances.append(self)

    def set_preconds(self, preconds):
        self.preconds = preconds

    def set_added_effects(self, added_effects):
        self.added_effects = added_effects

    def set_negative_effects(self, negative_effects):
        self.negative_effects = negative_effects


def operator_parser():