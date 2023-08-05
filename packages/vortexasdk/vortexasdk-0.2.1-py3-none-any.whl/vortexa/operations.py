from typing import List

from vortexasdk.client import default_client


class Reference:
    """Lookup Vortexa Reference Data using an entity ID."""

    def __init__(self, resource):
        self._resource = resource

    def reference(self, id: str):
        """

        # Arguments
            id: ID of the entity we're searching

        # Returns
        An entity matching the ID

        # Examples

            >>> Reference("/reference/geographies").reference(id='cfb8c4ef76585c3a37792b643791a0f4ff6d5656d5508927d8017319e21f2fca')

        """
        return default_client().get_reference(self._resource, id)


class Search:
    """Search Vortexa Reference Data."""

    def __init__(self, resource):
        """

        # Arguments
            resource: Appropriate search resource

        """
        self._resource = resource

    def search(self, **params) -> List[dict]:
        """

        # Arguments
            params: Search parameters

        # Returns
        VortexaAPI call matching vessels

        # Examples

            >>> Search("/reference/vessels").search(term="DHT")

        """

        return default_client().search(self._resource, **params)
