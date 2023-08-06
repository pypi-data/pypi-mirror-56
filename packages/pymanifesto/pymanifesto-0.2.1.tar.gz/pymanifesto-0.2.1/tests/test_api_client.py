#!/usr/bin/env python

"""Tests for the `pymanifesto` API client."""


import random
import string
import unittest
import urllib.error
from unittest import mock

from pymanifesto.pymanifesto import API, DatasetVersion


def _generate_random_key(key_length: int = 32) -> str:
    """Generates a random key based on the Manifesto Project API key schema."""
    return "".join(random.choices(string.printable, k=key_length))


class TestAPIClient(unittest.TestCase):
    """Tests for the API client defined in `pymanifesto`."""

    def setUp(self):
        self.api_key = _generate_random_key()

    def test_create_api_client(self):
        """Test the creation of the API client."""
        api = API(api_key=self.api_key)

        self.assertEqual(api.api_key, self.api_key)


class TestListCoreVersions(unittest.TestCase):
    """Tests for the API client method `list_core_versions`."""

    def setUp(self):
        self.api = API(api_key=_generate_random_key())
        self.datasets = b'{"datasets":[{"id":"MPDS2012a","name":"Manifesto Project Dataset (version 2012a)"},{"id":"MPDS2012b","name":"Manifesto Project Dataset (version 2012b)"}]}'
        self.datasets_sa = b'{"datasets":[{"id":"MPDSSA2015a","name":"Manifesto Project Dataset: South America (version 2015a)"},{"id":"MPDSSA2016b","name":"Manifesto Project Dataset: South America (version 2016b)"}]}'

    @mock.patch("urllib.request.urlopen")
    def test_call_list_core_versions_without_optional_parameter(self, patched_urlopen):
        """Calling the method without the optional parameter returns a list of core dataset versions."""
        expected = [
            DatasetVersion(
                id="MPDS2012a", name="Manifesto Project Dataset (version 2012a)"
            ),
            DatasetVersion(
                id="MPDS2012b", name="Manifesto Project Dataset (version 2012b)"
            ),
        ]

        patched_read = lambda: self.datasets
        patched_urlopen.return_value.__enter__.return_value.read = patched_read
        actual = self.api.list_core_versions()
        self.assertListEqual(actual, expected)

    @mock.patch("urllib.request.urlopen")
    def test_call_list_core_versions_with_optional_parameter(self, patched_urlopen):
        """
        Calling the method with the optional parameter returns a list of core dataset versions
        with their `kind` restricted by the parameter.
        """
        expected = [
            DatasetVersion(
                id="MPDSSA2015a",
                name="Manifesto Project Dataset: South America (version 2015a)",
            ),
            DatasetVersion(
                id="MPDSSA2016b",
                name="Manifesto Project Dataset: South America (version 2016b)",
            ),
        ]

        kind = "south_america"
        patched_read = lambda: self.datasets_sa
        patched_urlopen.return_value.__enter__.return_value.read = patched_read
        actual = self.api.list_core_versions(kind=kind)
        self.assertEqual(actual, expected)

    @mock.patch("urllib.request.urlopen")
    def test_call_list_core_versions_with_unknown_parameter_value(
        self, patched_urlopen
    ):
        """
        Calling the method with a parameter value that is not present in the Manifesto
        Project's database, a `ValueError` is raised.
        """
        kind = "unknown_kind"
        patched_read = urllib.error.HTTPError(
            url="", code=404, msg="", hdrs={}, fp=None
        )
        patched_urlopen.side_effect = patched_read
        with self.assertRaises(ValueError) as cm:
            self.api.list_core_versions(kind=kind)

        self.assertEqual(
            str(cm.exception), f"The kind {kind} is not known to the database."
        )
