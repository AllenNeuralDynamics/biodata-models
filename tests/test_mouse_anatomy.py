"""Test mouse anatomy class methods"""

import unittest

from unittest.mock import patch
from biodata_models.mouse_anatomy import search_emapa_exact_match, get_emapa_id
from biodata_models.mouse_anatomy import MouseAnatomy, MouseAnatomyModel, MouseEmgMuscles, Registry


class MouseAnatomyTests(unittest.TestCase):
    """Tests mouse anatomy"""

    @patch("biodata_models.mouse_anatomy.requests.get")
    def test_search_emapa_exact_match(self, mock_get):
        """Test search_emapa_exact_match function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = search_emapa_exact_match("Test Label")
        expected = [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={"q": "Test Label", "ontology": "emapa", "type": "class", "rows": 1},
            timeout=30,
        )

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        with self.assertRaises(Exception):
            search_emapa_exact_match("Test Label")

    @patch("biodata_models.mouse_anatomy.requests.get")
    def test_get_emapa_id(self, mock_get):
        """Test get_emapa_id function"""
        mock_response = {"response": {"docs": [{"iri": "http://example.com/EMAPA_12345", "label": "Test Label"}]}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_emapa_id("Test Label")
        expected = "12345"
        self.assertEqual(result, expected)

    @patch("biodata_models.mouse_anatomy.requests.get")
    def test_get_emapa_id_no_match(self, mock_get):
        """Test get_emapa_id function with no match"""
        mock_response = {"response": {"docs": []}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_emapa_id("Nonexistent Label")
        self.assertIsNone(result)


class MouseAnatomyMetaTests(unittest.TestCase):
    """Tests MouseAnatomyMeta class"""

    @patch("biodata_models.mouse_anatomy.get_emapa_id")
    def test_getattribute_existing_attribute(self, mock_get_emapa_id):
        """Test __getattribute__ for existing attribute"""
        mock_get_emapa_id.return_value = "12345"
        result = MouseAnatomy.ANATOMICAL_STRUCTURE
        expected = MouseAnatomyModel(
            name="Anatomical structure",
            registry=Registry.EMAPA,
            registry_identifier="0",
        )
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.registry, expected.registry)
        self.assertEqual(result.registry_identifier, expected.registry_identifier)
        mock_get_emapa_id.assert_not_called()

    @patch("biodata_models.mouse_anatomy.get_emapa_id")
    def test_getattribute_uses_csv_identifier(self, mock_get_emapa_id):
        """Test generated attributes use their checked-in EMAPA identifiers"""
        result = MouseAnatomy.HEART

        self.assertEqual(result.name, "heart")
        self.assertEqual(result.registry_identifier, "16105")
        mock_get_emapa_id.assert_not_called()

    @patch("biodata_models.mouse_anatomy.get_emapa_id")
    def test_getattribute_nonexistent_attribute(self, mock_get_emapa_id):
        """Test __getattribute__ for nonexistent attribute"""
        mock_get_emapa_id.return_value = None
        with self.assertRaises(AttributeError):
            MouseAnatomy.NONEXISTENT_ATTRIBUTE

        # Dynamic values still use the OLS fallback.
        with self.assertRaises(ValueError):
            MouseEmgMuscles.DELTOID

    def test_getattribute_magic_method(self):
        """Test __getattribute__ for magic method"""
        result = MouseAnatomy.__name__
        expected = "MouseAnatomy"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
