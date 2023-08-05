import typing

from leanbase import constants
from leanbase.storage import FeatureStore, SegmentStore
from leanbase.evaluate import evaluate

class User(object):
    def __init__(self, attributes:typing.Dict, feature_store:FeatureStore, segment_store:SegmentStore):
        self._attributes = attributes
        self._feature_store = feature_store
        self._segment_store = segment_store

    def _get_staff_segment(self):
        return self._segment_store.get_segment(constants.STAFF_SEGMENT_INTERNAL_ID)

    
    def can_access(self, feature_key:str):
        feature = self._feature_store.get_feature(feature_key)
        if feature:
            return evaluate(self._attributes, feature, self._get_staff_segment())
        
        # If the feature itself does not exist, then allow the user access.
        return True