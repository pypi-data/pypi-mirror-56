import os
from abc import ABC
from typing import List

import requests
from requests import Response

from vortexasdk.api.id import ID
from vortexasdk.endpoints.endpoints import API_URL


class AbstractVortexaClient(ABC):
    """Base client."""

    def get_reference(self, resource: str, id: ID) -> str:
        """Lookup reference data."""
        raise NotImplementedError

    def search(self, resource: str, **data) -> List:
        """Search."""
        raise NotImplementedError


class VortexaClient(AbstractVortexaClient):
    """The API client responsible for calling Vortexa's Public API."""

    _DEFAULT_PAGE_LOAD_SIZE = 10000

    def __init__(self, **kwargs):
        self.api_key = kwargs["api_key"]

    def get_reference(self, resource: str, id: ID) -> str:
        """Lookup reference data."""
        url = self._create_url(f'{resource}/{id}')
        response = requests.get(url)
        return self._handle_response(response)['data']

    def search(self, resource: str, **data) -> List:
        """Search using `resource` using `**data` as filter params."""
        url = self._create_url(resource)

        payload = {k: v for k, v in data.items() if v is not None}

        total = self._sent_post_request(url, payload, size=1, offset=0)['total']

        size = data.get('size', 1000)
        offsets = [i for i in range(0, total, size)]

        pmap = map
        # pmap = Pool(N_PARALLELISM * 2).map

        send_request = lambda x: self._sent_post_request(url, payload, size, x)['data']

        responses = list(pmap(send_request, offsets))

        flattened = [x for y in responses for x in y]

        assert len(flattened) == total
        return flattened

    def _create_url(self, path: str) -> str:
        return f'{API_URL}{path}?apikey={self.api_key}'

    def _sent_post_request(self, url, payload, size, offset):
        print(f'Sending post request, offset: {offset}, size: {size}')
        payload["offset"] = offset
        payload["cm_offset"] = offset
        payload["size"] = size
        payload["cm_size"] = size

        response = requests.post(url, json=payload)

        print(f'Post request received {len(response.json()["data"])} items')

        return self._handle_response(response, payload)

    @staticmethod
    def _handle_response(response: Response, payload=None):
        if response.ok:
            return response.json()
        else:
            print(response.reason)
            print(response.json())
            print(f'payload: {payload}')
            raise Exception(response)


__client__ = None


def default_client() -> VortexaClient:
    """Instantiate VortexaClient as global variable."""
    global __client__

    if __client__ is None:
        __client__ = create_client()

    return __client__


def create_client() -> VortexaClient:
    """Create new VortexaClient."""
    print("Creating new VortexaClient")
    try:
        api_key = os.environ["VORTEXA_API_KEY"]
    except KeyError:
        raise KeyError("VORTEXA_API_KEY environment variable is required to use the VortexaSDK")
    return VortexaClient(api_key=api_key)


def set_client(client) -> None:
    """Set the global client, used by all endpoints."""
    global __client__
    __client__ = client
    print(f'global __client__ has been set {__client__.__class__.__name__} \n')
