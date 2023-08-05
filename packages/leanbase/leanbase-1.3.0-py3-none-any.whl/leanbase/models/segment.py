import enum

class ConditionJoinOperator(enum.Enum):
    """ How are conditions joined together? """
    
    OR = 'or'
    AND = 'and'


class SegmentDefinition(object):
    """ Describes the matching criteria for a segment. """

    def __init__(self, conditions=[], operator=ConditionJoinOperator.OR):
        self.conditions = conditions
        self.operator = operator
