"""
This module defines the Simiotics client class, which can be used to access Simiotics APIs from
Python environments.
"""

import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar

import requests

from .source_types import SOURCE_TYPES

ClientType = TypeVar('ClientType', bound='SimioticsRESTClient')

class SimioticsRESTClient:
    """
    Simiotics REST client:
    Provides low-level interface to the Simiotics APIs. Contains one method for each allowed HTTP
    verb at each REST endpoint.
    """
    def __init__(self, api_url: str, auth_token: str, timeout: float = 10.0) -> None:
        """
        Instantiate a SimioticsRESTClient

        Args:
        api_url
            URL for the Simiotics API instance that this client uses
            (e.g. https://api.simiotics.com)
        auth_token
            Authentication token for Simiotics APIs. Will be passed in the Authorization header on
            HTTP requests as f"Authorization: Token {simiotics_token}"
        timeout
            Timeout to apply to individual Simiotics API requests (default 10 seconds)

        Returns: None
        """
        self.api_url = api_url
        self.auth_token = auth_token
        self.timeout = timeout

        self.standard_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.auth_token}',
        }

    @classmethod
    def from_env(cls: Type[ClientType]) -> ClientType:
        """
        Instantiates a SimioticsRESTClient using values from the environment. Expects the following
        environment variables to be defined:
        * SIMIOTICS_API_URL
        * SIMIOTICS_TOKEN
        * SIMIOTICS_TIMEOUT (optional - default value is 10.0)
        """
        api_url = os.environ.get('SIMIOTICS_API_URL')
        if api_url is None:
            raise ValueError('SIMIOTICS_API_URL environment variable not defined')

        auth_token = os.environ.get('SIMIOTICS_TOKEN')
        if auth_token is None:
            raise ValueError('SIMIOTICS_TOKEN environment variable not defined')

        raw_timeout = os.environ.get('SIMIOTICS_TIMEOUT', '10')
        timeout = float(raw_timeout)

        return cls(api_url, auth_token, timeout)

    def ping(self) -> Dict[str, str]:
        """
        Pings the API associated with this SimioticsRESTClient to check its health.
        """
        response = requests.get(
            f'{self.api_url}/ping',
            headers=self.standard_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def datasets_list(self, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Lists all datasets that the token-bearer has created against the given API

        Args:
        offset
            Starting index for the listing (0-indexed)
        limit
            Number of items to list

        Returns: JSON object representing listing of datasets
        """
        response = requests.get(
            f'{self.api_url}/datasets/',
            headers=self.standard_headers,
            timeout=self.timeout,
            params={
                'offset': offset,
                'limit': limit,
            }
        )
        response.raise_for_status()
        return response.json()

    def dataset_create(
            self,
            id: str,
            source_type: str,
            uri: str,
            description: Optional[str] = None,
        ) -> Dict[str, Any]:
        """
        Creates a new dataset for the token-bearer

        Args:
        id
            ID for the dataset (must be globally unique)
        source_type
            Source type for the dataset (must be a key for the SOURCE_TYPES dictionary in
            source_types.py)
        uri
            URI for the source
        description
            (Optional) Human-readable description for the dataset

        Returns: JSON object representing the dataset that was created
        """
        if source_type not in SOURCE_TYPES:
            raise ValueError(
                f'Invalid source_type={source_type}. Must be one of {list(SOURCE_TYPES.keys())}'
            )
        response = requests.post(
            f'{self.api_url}/datasets/',
            headers=self.standard_headers,
            timeout=self.timeout,
            json={
                'id': id,
                'source_type': source_type,
                'uri': uri,
                'description': description,
            },
        )
        response.raise_for_status()
        return response.json()

    def dataset_get(self, id: str) -> Dict[str, Any]:
        """
        Gets a dataset by its id

        Args:
        id
            ID for the dataset

        Returns: JSON object representing the retrieved dataset
        """
        response = requests.get(
            f'{self.api_url}/datasets/{id}/',
            headers=self.standard_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def samples_list(self, dataset_id: str, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Lists all datasets that the token-bearer has created against the given API

        Args:
        dataset_id
            ID of dataset for which samples should be listed
        offset
            Starting index for the listing (0-indexed)
        limit
            Number of items to list

        Returns: JSON object representing listing of samples within the dataset with the given
        dataset_id
        """
        response = requests.get(
            f'{self.api_url}/datasets/{dataset_id}/samples/',
            headers=self.standard_headers,
            timeout=self.timeout,
            params={
                'offset': offset,
                'limit': limit,
            }
        )
        response.raise_for_status()
        return response.json()

    def sample_create(
            self,
            dataset_id: str,
            sample_content: str,
            attributes: List[Dict[str, Optional[str]]],
        ) -> Dict[str, Any]:
        """
        Creates a new sample within a dataset

        Args:
        dataset_id
            ID for the dataset within which to register a sample
        sample_content
            Content of the sample
        attributes
            List of dictionaries of the form {'key': '<str>', 'value': '<Optional[str]>'}
        description
            (Optional) Human-readable description for the dataset

        Returns: JSON object representing the sample that was created
        """
        response = requests.post(
            f'{self.api_url}/datasets/{dataset_id}/samples/',
            headers=self.standard_headers,
            timeout=self.timeout,
            json={
                'content': sample_content,
                'attributes': attributes,
            },
        )
        response.raise_for_status()
        return response.json()

    def sample_get(self, dataset_id: str, sample_id: str) -> Dict[str, Any]:
        """
        Gets a dataset by its id

        Args:
        dataset_id
            ID for the dataset that the sample belongs to
        sample_id
            ID for the sample itself

        Returns: JSON object representing the retrieved sample
        """
        response = requests.get(
            f'{self.api_url}/datasets/{dataset_id}/samples/{sample_id}',
            headers=self.standard_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def sample_attribute_create(
            self,
            dataset_id: str,
            sample_id: str,
            key: str,
            value: Optional[str] = None
        ) -> Dict[str, Any]:
        """
        Tag a given sample with an attribute (key-value pair)

        Args:
        dataset_id
            ID for the dataset that the sample belongs to
        sample_id
            ID for the sample
        key
            Attribute key
        value
            (Optional) Attribute value

        Returns: JSON representation of the new attribute associated with the sample
        """
        response = requests.post(
            f'{self.api_url}/datasets/{dataset_id}/samples/{sample_id}/tag',
            headers=self.standard_headers,
            timeout=self.timeout,
            json={
                'key': key,
                'value': value,
            },
        )
        response.raise_for_status()
        return response.json()
