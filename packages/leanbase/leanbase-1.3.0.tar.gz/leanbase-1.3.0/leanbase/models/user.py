import typing

from leanbase.storage import FeatureStore, SegmentStore
from leanbase.evaluate import evaluate

class User(object):
    def __init__(self, attributes:typing.Dict, feature_store:FeatureStore, segment_store:SegmentStore):
        self._attributes = attributes
        self._feature_store = feature_store
    
    def can_access(self, feature_key:str):
        feature = self._feature_store.get_feature(feature_key)
        if feature:
            return evaluate(self._attributes, feature)
        
        # If the feature itself does not exist, then allow the user access.
        return True