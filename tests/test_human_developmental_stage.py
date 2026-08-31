"""Test human developmental stage class methods"""

import unittest

from unittest.mock import patch
from biodata_models.human_developmental_stage import search_hsapdv_exact_match, get_hsapdv_id
from biodata_models.human_developmental_stage import (
    HumanDevelopmentalStage,
    HumanDevelopmentalStageModel,
    Registry,
)


class HumanDevelopmentalStageTests(unittest.TestCase):
    """Tests human developmental stage"""

    @patch("biodata_models.human_developmental_stage.requests.get")
    def test_search_hsapdv_exact_match(self, mock_get):
        """Test search_hsapdv_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/HsapDv_0000258", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_hsapdv_exact_match("Test Label")
        expected = [{"iri": "http://example.com/HsapDv_0000258", "label": "Test Label"}]
        self.assertEqual(result, expected)

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_hsapdv_exact_match("Test Label")

    @patch("biodata_models.human_developmental_stage.requests.get")
    def test_get_hsapdv_id(self, mock_get):
        """Test get_hsapdv_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/HsapDv_0000258", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_hsapdv_id("Test Label")
        expected = "0000258"
        self.assertEqual(result, expected)

    @patch("biodata_models.human_developmental_stage.requests.get")
    def test_get_hsapdv_id_no_match(self, mock_get):
        """Test get_hsapdv_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_hsapdv_id("Nonexistent Label")
        self.assertIsNone(result)


class HumanDevelopmentalStageMetaTests(unittest.TestCase):
    """Tests HumanDevelopmentalStageMeta class"""

    @patch("biodata_models.human_developmental_stage.get_hsapdv_id")
    def test_getattribute_existing_attribute(self, mock_get_hsapdv_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_hsapdv_id.return_value = "0000258"
        result = HumanDevelopmentalStage.ADULT_STAGE
        expected = HumanDevelopmentalStageModel(
            name="adult stage",
            registry=Registry.HSAPDV,
            registry_identifier="0000258",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)

    @patch("biodata_models.human_developmental_stage.get_hsapdv_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_hsapdv_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_hsapdv_id.return_value = None
        with self.assertRaises(AttributeError):
            HumanDevelopmentalStage.NONEXISTENT_ATTRIBUTE

        # this is a real attribute, but we're faking that it doesn't exist in the registry
        with self.assertRaises(ValueError):
            HumanDevelopmentalStage.ADULT_STAGE

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = HumanDevelopmentalStage.__name__
        expected = "HumanDevelopmentalStage"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
