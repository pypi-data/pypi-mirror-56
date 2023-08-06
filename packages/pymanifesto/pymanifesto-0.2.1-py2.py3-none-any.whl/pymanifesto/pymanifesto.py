"""
`pymanifesto` provides the API client as well as utility classes and functions.
"""
import json
import typing
from dataclasses import dataclass
from urllib import error, parse, request


class API:
    """
    `API` is the central entry point for the Manifesto Project API.

    It encapsulates the `api_key` and exposes the API's endpoints.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    @property
    def api_root(self) -> str:
        """
        The API's root URL as defined by:
            https://manifestoproject.wzb.eu/information/documents/api
        """
        return "https://manifesto-project.wzb.eu/tools"

    def list_core_versions(
        self, kind: typing.Optional[str] = None
    ) -> typing.List["DatasetVersion"]:
        """
        Lists all core dataset versions.
        """
        options = {}
        if kind is not None:
            options.update({"kind": kind})

        data = self._make_request(endpoint="api_list_core_versions", options=options)

        try:
            result = [DatasetVersion(**dv) for dv in data["datasets"]]
        except KeyError:
            raise ValueError(f"The kind {kind} is not known to the database.")
        else:
            return result

    def _make_request(self, endpoint: str, options: typing.Dict) -> typing.Dict:
        url = f"{self.api_root}/{endpoint}.json"

        if options:
            encoded_options = parse.urlencode(options)
            url += f"?{encoded_options}"

        try:
            with request.urlopen(url) as content:
                data = content.read().decode("utf-8")
        except error.HTTPError:
            result = {"error": "Element not found"}
        else:
            result = json.loads(data)

        return result


@dataclass
class DatasetVersion:
    """`DatasetVersion` models the objects returned by calling `API.list_core_versions`"""

    id: str  # pylint: disable=invalid-name
    name: str
