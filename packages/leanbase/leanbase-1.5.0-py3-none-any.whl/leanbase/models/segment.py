import enum
import typing

from .condition import Condition

class ConditionCombinator(enum.Enum):
    """ How are conditions joined together? """
    
    OR = 'or'
    AND = 'and'


class SegmentDefinition(object):
    """ Describes the matching criteria for a segment. """

    def __init__(self, conditions=[], combinator=ConditionCombinator.OR):
        self.conditions = conditions
        self.combinator = combinator


    @classmethod
    def from_encoding(cls, mc:typing.List[typing.Tuple[str, str, str, str]], cmb:str):
        conditions = list(map(Condition.from_encoding, mc))
        if cmb in ['OR', 'or', 'Or']:
            combinator = ConditionCombinator.OR
        else:
            combinator = ConditionCombinator.AND

        return cls(conditions=conditions, combinator=combinator)