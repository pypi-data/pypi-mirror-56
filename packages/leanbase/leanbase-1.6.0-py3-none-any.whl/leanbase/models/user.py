import typing
from jwt import encode

from leanbase import constants
from leanbase.storage import FeatureStore, SegmentStore
from leanbase.evaluate import evaluate
from leanbase.client import LBClient

class User(object):
    def __init__(self, attributes:typing.Dict, client:LBClient):
        self._attributes = attributes
        self._feature_store = client.get_feature_store()
        self._segment_store = client.get_segment_store()
        self._client = client

    def _get_staff_segment(self):
        return self._segment_store.get_segment(constants.STAFF_SEGMENT_INTERNAL_ID)

    def can_access(self, feature_key:str):
        feature = self._feature_store.get_feature(feature_key)
        if feature:
            return evaluate(self._attributes, feature, self._get_staff_segment())
        
        # If the feature itself does not exist, then allow the user access.
        return True

    def get_user_token(self):
        user_token_secret = self._client.get_config().user_token_secret
        payload = {
            "teamId": self._client.get_config().team_id,
            "user": self._attributes
        }
        return encode(payload, user_token_secret, algorithm='HS256')


def _get_team_secret(team_id):
    """ hash the team_id with a key to obtain the team_secret. This could later
    be moved to maintaining a key on the lbapp system. """
    key_byte_array = bytearray()
    key_byte_array.extend(config.JWT_HMAC_SECRET.encode('utf-8'))
    return hmac.new(key_byte_array, team_id.encode('utf-8')).hexdigest()