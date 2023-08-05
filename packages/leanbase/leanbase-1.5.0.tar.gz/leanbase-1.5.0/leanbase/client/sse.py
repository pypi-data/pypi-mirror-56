import six
from six.moves.urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin
import sseclient
import json

from leanbase.models.config import LBClientConfig

def process_sse(event):
    return json.loads(event.data)

class SSEMessageSource(six.Iterator):
    def __init__(self, config:LBClientConfig=None):
        if config == None:
            raise BadConfigurationException("Message source must be init with a config")
        
        self._config = config

        headers = {
            'X-API-Token': self._config.api_key,
        }
        self._client = sseclient.SSEClient(self._build_url(), chunk_size=64, headers=headers)

    def _build_url(self):
        parts = urlparse(self._config.convey_host)
        path = urljoin(parts.path, 'v1/notify/{}/stream'.format(self._config.team_id))
        return urlunparse((parts.scheme, parts.netloc, path, parts.params, parts.query, parts.fragment))
        
    def __iter__(self):
        return map(process_sse, 
            filter(
                lambda ev: ev.event == 'update',
                self._client
            )
        )