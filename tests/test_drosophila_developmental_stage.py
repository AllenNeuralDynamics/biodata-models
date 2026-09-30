"""Test drosophila developmental stage class methods"""

import unittest

from unittest.mock import patch
from biodata_models.drosophila_developmental_stage import search_fbdv_exact_match, get_fbdv_id
from biodata_models.drosophila_developmental_stage import (
    DrosophilaDevelopmentalStageLookup,
    DrosophilaDevelopmentalStageModel,
    Registry,
)


class DrosophilaDevelopmentalStageTests(unittest.TestCase):
    """Tests drosophila developmental stage"""

    @patch("biodata_models.drosophila_developmental_stage.requests.get")
    def test_search_fbdv_exact_match(self, mock_get):
        """Test search_fbdv_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/FBdv_00005369", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_fbdv_exact_match("Test Label")
        expected = [{"iri": "http://example.com/FBdv_00005369", "label": "Test Label"}]
        self.assertEqual(result, expected)

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_fbdv_exact_match("Test Label")

    @patch("biodata_models.drosophila_developmental_stage.requests.get")
    def test_get_fbdv_id(self, mock_get):
        """Test get_fbdv_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/FBdv_00005369", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_fbdv_id("Test Label")
        expected = "00005369"
        self.assertEqual(result, expected)

    @patch("biodata_models.drosophila_developmental_stage.requests.get")
    def test_get_fbdv_id_no_match(self, mock_get):
        """Test get_fbdv_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_fbdv_id("Nonexistent Label")
        self.assertIsNone(result)


class DrosophilaDevelopmentalStageMetaTests(unittest.TestCase):
    """Tests DrosophilaDevelopmentalStageMeta class"""

    @patch("biodata_models.drosophila_developmental_stage.get_fbdv_id")
    def test_getattribute_existing_attribute(self, mock_get_fbdv_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_fbdv_id.return_value = "00005369"
        result = DrosophilaDevelopmentalStageLookup.ADULT_STAGE
        expected = DrosophilaDevelopmentalStageModel(
            name="adult stage",
            registry=Registry.FBDV,
            registry_identifier="00005369",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)

    @patch("biodata_models.drosophila_developmental_stage.get_fbdv_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_fbdv_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_fbdv_id.return_value = None
        with self.assertRaises(AttributeError):
            DrosophilaDevelopmentalStageLookup.NONEXISTENT_ATTRIBUTE

        # this is a real attribute, but we're faking that it doesn't exist in the registry
        with self.assertRaises(ValueError):
            DrosophilaDevelopmentalStageLookup.ADULT_STAGE

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = DrosophilaDevelopmentalStageLookup.__name__
        expected = "DrosophilaDevelopmentalStageLookup"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
