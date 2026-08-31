"""Test C. elegans developmental stage class methods"""

import unittest

from unittest.mock import patch
from biodata_models.celegans_developmental_stage import search_wbls_exact_match, get_wbls_id
from biodata_models.celegans_developmental_stage import (
    CElegansDevelopmentalStage,
    CElegansDevelopmentalStageModel,
    Registry,
)


class CElegansDevelopmentalStageTests(unittest.TestCase):
    """Tests C. elegans developmental stage"""

    @patch("biodata_models.celegans_developmental_stage.requests.get")
    def test_search_wbls_exact_match(self, mock_get):
        """Test search_wbls_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/WBls_0000825", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_wbls_exact_match("Test Label")
        expected = [{"iri": "http://example.com/WBls_0000825", "label": "Test Label"}]
        self.assertEqual(result, expected)

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_wbls_exact_match("Test Label")

    @patch("biodata_models.celegans_developmental_stage.requests.get")
    def test_get_wbls_id(self, mock_get):
        """Test get_wbls_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/WBls_0000825", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_wbls_id("Test Label")
        expected = "0000825"
        self.assertEqual(result, expected)

    @patch("biodata_models.celegans_developmental_stage.requests.get")
    def test_get_wbls_id_no_match(self, mock_get):
        """Test get_wbls_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_wbls_id("Nonexistent Label")
        self.assertIsNone(result)


class CElegansDevelopmentalStageMetaTests(unittest.TestCase):
    """Tests CElegansDevelopmentalStageMeta class"""

    @patch("biodata_models.celegans_developmental_stage.get_wbls_id")
    def test_getattribute_existing_attribute(self, mock_get_wbls_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_wbls_id.return_value = "0000825"
        result = CElegansDevelopmentalStage.C__ELEGANS_LIFE_STAGE
        expected = CElegansDevelopmentalStageModel(
            name="C. elegans life stage",
            registry=Registry.WBLS,
            registry_identifier="0000825",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)

    @patch("biodata_models.celegans_developmental_stage.get_wbls_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_wbls_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_wbls_id.return_value = None
        with self.assertRaises(AttributeError):
            CElegansDevelopmentalStage.NONEXISTENT_ATTRIBUTE

        # this is a real attribute, but we're faking that it doesn't exist in the registry
        with self.assertRaises(ValueError):
            CElegansDevelopmentalStage.C__ELEGANS_LIFE_STAGE

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = CElegansDevelopmentalStage.__name__
        expected = "CElegansDevelopmentalStage"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
