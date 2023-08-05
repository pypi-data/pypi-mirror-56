from threading import Event
import typing

from leanbase import exceptions
from leanbase.models.config import build_config
from leanbase.models.user import User
from leanbase.client import LBClient
from leanbase.storage import SegmentStore, FeatureStore

_configuration = None
_client = None

_ready_event = Event()

def configure(api_key=None, **kwargs):
    """ Configure the leanbase client. Within a runtime, this should only be
    done once. Attempting to do this multiple times will throw an exception.
    Calling configure sets about a chain of actions:
    1. create the worker threads, and queues
    2. setup a connection with the convey endpoint, download the first set of 
       segment/feature definitions

    Internally, the configuration object is passed to all worker threads. This 
    is an immutable object and is thread safe.

    :param api_key: The API key supplied to you via https://app.leanbase.io/
    :type api_key: str

    :param **kwargs: any additional options you would like to pass. Refer docs
                     for details
    :type **kwargs: variadic keyword arguments

    :rtype: None
    """
    global _configuration, _client, _ready_event
    if not _configuration == None:
        raise exceptions.ReconfigurationException
    
    _configuration = build_config(api_key=api_key, **kwargs)

    _client = LBClient(
        config=_configuration,
        segment_store=SegmentStore(),
        feature_store=FeatureStore(),
        ready_event=_ready_event,
    )

def await_initialisation(timeout=1.0):
    _ready_event.wait(timeout)

def user(user_attributes:typing.Dict):
    global _client
    if not _client:
        raise exceptions.NotConfiguredException

    return User(user_attributes, _client._feature_store, _client._segment_store)