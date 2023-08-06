"""
MeaPy - Python API Wrapper for Measurement Data
"""
import requests
import json
from .loadingconfig import LoadingConfig
from .measurement import Measurement


class MeaPy:
    """Wrapper object for the MaDaM system. Requires an url string and an auth string for creation."""

    def __init__(self, url: str, auth: str):
        """Creates a MaDaM wrapper object. Requires an url and auth parameter.

        Parameters
        ----------
        url : str
            the URL to the MaDaM system
        auth : str
            authentication info which can either be a sessionId oder accessToken
        """
        self.url = url
        self.auth = auth
        self.offset = None

    def search(self, query: str, limit=100, offset=None, clearOffset=False) -> object:
        """Searches for a query string in the MaDaM system and returns a list of found measurements.

        Parameters
        ----------

        Returns
        -------
        map
            a map of measurements that are found for the given query
        """
        newOffset = offset
        if not clearOffset:
            newOffset = self.offset

        payload = {
            'queryString': query,
            'limit': limit,
            'offset': newOffset,
            'expansionOptions': {
                'base': {
                    'type': 'all',
                    'includeTopLevelFields': True,
                    'includeRecursiveFields': False,
                    'includeTopLevelLabels': False,
                    'includeRecursiveLabels': False,
                    'ignoreReferenceLists': True,
                    'recursionDepth': 0
                }
            }
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self.auth
        }
        response = requests.post(self.url + 'backend/api/v1/search/search',
                          data=json.dumps(payload), headers=headers)
        responseJson = response.json()
        self.offset = responseJson.get('offset')
        documentGraph = responseJson.get('documentGraph')
        documents = documentGraph.get('documents')
        return list(map(
            lambda docRef: Measurement(documents.get(
                docRef.get('type')).get(docRef.get('id'))),
            documentGraph.get('documentRefs')
        ))

    def load(self, measurement: object, config: LoadingConfig) -> list:
        return []

    def loadList(self, measurements: list, config: LoadingConfig) -> object:
        return {}
