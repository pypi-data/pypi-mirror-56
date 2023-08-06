import threading

from leanbase.models.segment import SegmentDefinition
from leanbase.models.feature import FeatureDefinition

class SegmentStore(object):
    def __init__(self):
        self._store = {}
        self._lock = threading.RLock()
    
    def get_segment(self, segment_id)->SegmentDefinition:
        with self._lock:
            if segment_id in self._store:
                return self._store[segment_id]
    
    def set_segment(self, segment_id:str, segment_definition:SegmentDefinition):
        with self._lock:
            self._store[segment_id] = segment_definition


class FeatureStore(object):
    def __init__(self):
        self._store = {}
        self._lock = threading.RLock()

    def get_feature(self, feature_id:str)->FeatureDefinition:
        with self._lock:
            if feature_id in self._store:
                return self._store[feature_id]
            
    def set_feature(self, feature_id:str, feature_definition:FeatureDefinition):
        with self._lock:
            self._store[feature_id] = feature_definition