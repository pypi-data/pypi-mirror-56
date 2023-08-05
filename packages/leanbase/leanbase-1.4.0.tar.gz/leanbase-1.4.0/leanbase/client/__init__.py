import threading
import logging

from leanbase.exceptions import BadConfigurationException
from leanbase.models.config import LBClientConfig
from leanbase.storage.inmemory import SegmentStore, FeatureStore
from leanbase.tasks.workers import FeatureSyncWorker, SegmentSyncWorker, ConveyEventsWorker


class LBClient(object):
    """ Given a message sources, processes the messages in order, populates and
    updates segment and feature stores. """ 

    def __init__(
            self,
            config:LBClientConfig=None,
            segment_store:SegmentStore=None,
            feature_store:FeatureStore=None,
            ready_event:threading.Event=None
        ):
        if config == None:
            raise BadConfigurationException("LB Client should be initialized with a configuration")
        self._config = config

        self._ready_event = ready_event
        self._ready_states = {
            'feature': threading.Event(),
            'segment': threading.Event(),
        }

        self._segment_store = segment_store
        self._feature_store = feature_store
        self._engage()
        self._await_initialization()

    def _await_initialization(self):
        # If all ready_states are fulfilled, set the ready_event.
        client = self
        for (key, event) in self._ready_states.items():
            def await_inner():
                event.wait()
                if all(map(lambda x: x.is_set(), client._ready_states.values())):
                    logging.info('All sync threads have initialized. Firing ready event.')
                    client._ready_event.set()

            threading.Thread(target=await_inner, name='{}.await-init'.format(key)).start()



    def _engage(self):
        threads = []

        t = SegmentSyncWorker(self._config, self._segment_store, init_event=self._ready_states['segment'])
        segment_sync_t = threading.Thread(name='segment.sync', target=t.start)
        segment_sync_t.start()
        threads.append(segment_sync_t)

        t = FeatureSyncWorker(self._config, self._feature_store, init_event=self._ready_states['feature'])
        feature_sync_t = threading.Thread(name='feature.sync', target=t.start)
        feature_sync_t.start()
        threads.append(feature_sync_t)

        t = ConveyEventsWorker(self._config)
        convey_events_t = threading.Thread(name='backend.listener', target=t.start)
        convey_events_t.start()
        threads.append(convey_events_t)


