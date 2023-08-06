#!/usr/bin/env python

"""This TestCase contains the functional tests for the `pymanifesto` library."""

import os
import unittest

from pymanifesto import pymanifesto


class TestPymanifesto(unittest.TestCase):
    """Tests for `pymanifesto` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.api_key = os.getenv("API_KEY", "")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_user_can_list_core_versions(self):
        """
        As a user, I want to be able to list the core dataset version.
        """
        # Create API client
        api = pymanifesto.API(self.api_key)

        # Request a list of core dataset versions
        dataset_versions = api.list_core_versions()

        # `dataset_versions` is a list of DatasetVersion object.
        for version in dataset_versions:
            self.assertIsInstance(version, pymanifesto.DatasetVersion)

    def test_user_can_list_core_versions_with_optional_parameter(self):
        """
        As a user, I want to be able to list the core dataset version and supply an optional
        parameter to restrict the responses to a certain `kind` of dataset.
        """
        # Create API client
        api = pymanifesto.API(self.api_key)

        # Supply a `kind` of dataset
        kind = "south_america"

        # Request a list of core dataset versions restricted by `kind`
        dataset_versions = api.list_core_versions(kind=kind)

        # `dataset_versions` is a list of DatasetVersion object.
        for version in dataset_versions:
            self.assertIsInstance(version, pymanifesto.DatasetVersion)
            self.assertIn("South America", version.name)

    def test_user_cannot_list_core_versions_for_unknown_optional_parameter(self):
        """
        As a user, I want to be notified by an exception when I supply an unknown optional parameter.
        """
        # Create API client
        api = pymanifesto.API(self.api_key)

        # Supply an unknown `kind` of dataset
        kind = "unknown_kind"

        # Request a list of core dataset versions restricted by `kind`
        with self.assertRaises(ValueError) as cm:
            dataset_versions = api.list_core_versions(kind=kind)

        # And I want the error message to be clear and meaningful
        self.assertEqual(
            str(cm.exception), f"The kind {kind} is not known to the database."
        )
