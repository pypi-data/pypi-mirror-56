"""
Adapter to make requests to 17track API
"""
import json
from typing import Dict, NamedTuple, List, Union

import requests

from .utils import get_api_key

__all__ = (
    'Response',
    'Track17Client',
    'Track17Adapter'
)

Response = NamedTuple('Response', [
    ('status_code', int),
    ('data', Dict)
])


class Track17Client:
    API_BASE_URL = 'https://api.17track.net/track/'
    API_VERSION = 1

    def __init__(
        self,
        api_base_url: str = None,
        api_version: str = None,
    ):
        """
        Initializes api connector. Received parameters required to
        connect remote server.

        Args:
            api_base_url (str, optional): Base url used to construct url.
            api_version (str, optional): API version to use.
        """
        self.api_base_url = api_base_url or self.API_BASE_URL
        self.api_version = api_version or self.API_VERSION

    def get_base_headers(self) -> Dict:
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Content-Type": "application/json",
        }

    def get_auth_headers(self) -> Dict:
        return {
            "17token": get_api_key()
        }

    def construct_url(self, *args) -> str:
        """
        Returns url with joined args as parts of url.

        Args:
            *args: part of url.

        Returns:
            str: URL
        """
        url = self.api_base_url

        if self.api_version:
            url += f'v{self.api_version}/'

        if not args:
            return url

        joined_args = '/'.join([x.strip('/') for x in args])

        return f'{url}{joined_args}'

    def post(
        self,
        path: str,
        data: Dict = None,
        headers: Dict = None,
    ):
        """
        Private method used to send request to the remote REST API
        server.

        Args:
            path (str): Corresponding relative path to send request.
            data (Dict, optional): Params to send.
            headers (Dict, optional): Request headers.

        Returns:
            Response: requests' response instance.

        Raises:
            AttributeError: Unsupported method was used.
        """
        url = self.construct_url(path)

        if headers is None:
            headers = {}

        headers.update(self.get_base_headers())
        headers.update(self.get_auth_headers())

        response = requests.post(url, data, headers=headers)

        return Response(
            status_code=response.status_code,
            data=response.json()
        )


class Track17Adapter:
    api_client_class = Track17Client

    def __init__(self):
        self.api_client = self.api_client_class()

    @staticmethod
    def _prepare_numbers(*tracking_numbers: Union[Dict, str]) -> List:
        numbers = []
        for number in tracking_numbers:
            if isinstance(number, dict) and all(key in number for key in ['number', 'carrier']):
                numbers.append(number)
            elif isinstance(number, str):
                numbers.append({
                    "number": number
                })
        return numbers

    def register(self, *tracking_numbers: str) -> Response:
        """
        40 tracking numbers are allowed to submit for registration per time for the interface.

        Response:
            {
                "code": 0,
                "data": {
                    "accepted": [
                        {
                            "number": "RR123456789CN",
                            "carrier": 3011
                        }
                    ],
                    "rejected": [
                        {
                            "number": "1234",
                            "error": {
                                "code": -18010012,
                                "message": "The format of '1234' is invalid."
                            }
                        }
                    ]
                }
            }
        """
        data = self._prepare_numbers(*tracking_numbers)
        data = json.dumps(data)
        response = self.api_client.post(
            'register',
            data
        )
        return response

    def stop_track(self, *tracking_numbers: str) -> Response:
        """
        40 tracking numbers are allowed to submit per time for the interface.
        """
        data = self._prepare_numbers(*tracking_numbers)
        data = json.dumps(data)
        response = self.api_client.post(
            'stoptrack',
            data
        )
        return response

    def retrack(self, *tracking_numbers: str) -> Response:
        """
        40 tracking numbers are allowed to submit per time for the interface.
        """
        data = self._prepare_numbers(*tracking_numbers)
        data = json.dumps(data)
        response = self.api_client.post(
            'retrack',
            data
        )
        return response

    def get_track_info(self, *tracking_numbers: str) -> Response:
        """
        40 tracking numbers are allowed to submit per time for the interface.
        """
        data = self._prepare_numbers(*tracking_numbers)
        data = json.dumps(data)
        response = self.api_client.post(
            'gettrackinfo',
            data
        )
        return response
