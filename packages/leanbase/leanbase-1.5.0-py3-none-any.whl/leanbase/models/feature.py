import typing
import enum

from .segment import SegmentDefinition


class FeatureGlobalStatus(enum.Enum):
    """ Describes the global status of a feature. Can be either of 
    (DEV, STAFF, PARTIAL, GA). With GA, we can short circuit the evaluation. At
    STAFF, we must compare to the Staff segment. With Partial, we use the hashed
    arithmetic. """
    DEV = 'dev'
    STAFF = 'staff'
    PARTIAL = 'partial'
    GA = 'ga'


class FeatureDefinition(object):
    """ Encapsulates the definition of a feature on the server. Provides methods
    to aid evaluation. The segment values are merely segment_ids. """

    def __init__(
        self, 
        _id, 
        global_status,
        enabled_for_segments=[],
        suppressed_for_segments=[],
        rollout_percentage=None,
    ):
        self.id = _id
        self.global_status = global_status
        self.enabled_for_segments = enabled_for_segments
        self.suppressed_for_segments = suppressed_for_segments
        self.rollout_percentage = rollout_percentage

    @classmethod
    def from_encoding(
            cls,
            gs:str=None,
            id:str=None,
            es:typing.List[typing.Dict]=[],
            ss:typing.List[typing.Dict]=[],
            rp:int=None,
        ):
        if gs == 'dev':
            global_status = FeatureGlobalStatus.DEV
        elif gs == 'staff':
            global_status = FeatureGlobalStatus.STAFF
        elif gs == 'partial':
            global_status = FeatureGlobalStatus.PARTIAL
        else:
            global_status = FeatureGlobalStatus.GA

        return cls(
            id, global_status,
            enabled_for_segments=list(map(lambda seg_def: SegmentDefinition.from_encoding(**seg_def), es)),
            suppressed_for_segments=list(map(lambda seg_def: SegmentDefinition.from_encoding(**seg_def), ss)),
            rollout_percentage=rp
        )