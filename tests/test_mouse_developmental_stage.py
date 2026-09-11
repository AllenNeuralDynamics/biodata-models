"""Test mouse developmental stage class methods"""

import unittest

from unittest.mock import patch
from biodata_models.mouse_developmental_stage import search_mmusdv_exact_match, get_mmusdv_id
from biodata_models.mouse_developmental_stage import (
    MouseDevelopmentalStage,
    MouseDevelopmentalStageModel,
    Registry,
)


class MouseDevelopmentalStageTests(unittest.TestCase):
    """Tests mouse developmental stage"""

    @patch("biodata_models.mouse_developmental_stage.requests.get")
    def test_search_mmusdv_exact_match(self, mock_get):
        """Test search_mmusdv_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/MmusDv_0000177", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_mmusdv_exact_match("Test Label")
        expected = [{"iri": "http://example.com/MmusDv_0000177", "label": "Test Label"}]
        self.assertEqual(result, expected)

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_mmusdv_exact_match("Test Label")

    @patch("biodata_models.mouse_developmental_stage.requests.get")
    def test_get_mmusdv_id(self, mock_get):
        """Test get_mmusdv_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/MmusDv_0000177", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_mmusdv_id("Test Label")
        expected = "0000177"
        self.assertEqual(result, expected)

    @patch("biodata_models.mouse_developmental_stage.requests.get")
    def test_get_mmusdv_id_no_match(self, mock_get):
        """Test get_mmusdv_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_mmusdv_id("Nonexistent Label")
        self.assertIsNone(result)


class MouseDevelopmentalStageMetaTests(unittest.TestCase):
    """Tests MouseDevelopmentalStageMeta class"""

    @patch("biodata_models.mouse_developmental_stage.get_mmusdv_id")
    def test_getattribute_existing_attribute(self, mock_get_mmusdv_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_mmusdv_id.return_value = "0000000"
        result = MouseDevelopmentalStage.LIFE_CYCLE_STAGE
        expected = MouseDevelopmentalStageModel(
            name="life cycle stage",
            registry=Registry.MMUSDV,
            registry_identifier="0000000",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)

    @patch("biodata_models.mouse_developmental_stage.get_mmusdv_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_mmusdv_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_mmusdv_id.return_value = None
        with self.assertRaises(AttributeError):
            MouseDevelopmentalStage.NONEXISTENT_ATTRIBUTE

        # this is a real attribute, but we're faking that it doesn't exist in the registry
        with self.assertRaises(ValueError):
            MouseDevelopmentalStage.LIFE_CYCLE_STAGE

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = MouseDevelopmentalStage.__name__
        expected = "MouseDevelopmentalStage"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
