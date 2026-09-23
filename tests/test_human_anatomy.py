"""Tests for the Human Anatomy OLS4 lookup."""

import unittest
from unittest.mock import patch

from biodata_models.human_anatomy import HumanAnatomy, HumanAnatomyModel
from biodata_models.registries import Registry


class HumanAnatomyTests(unittest.TestCase):
    """Tests for FMA search and lookup behavior."""

    @patch("biodata_models.human_anatomy.requests.get")
    def test_search_by_name_returns_active_fma_terms(self, mock_get):
        """Non-exact search returns active FMA results in OLS relevance order."""
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "fma7088", "label": "Heart"},
                    {"obo_id": "fma0328405", "label": "Organ component of heart"},
                    {"obo_id": "DOID:123", "label": "Heart disease"},
                    {"obo_id": "fma999", "label": "Obsolete term", "is_obsolete": True},
                ]
            }
        }

        result = HumanAnatomy.search_by_name(" heart ", limit=2)

        self.assertEqual(
            result,
            [
                HumanAnatomyModel(name="Heart", registry_identifier="fma7088"),
                HumanAnatomyModel(name="Organ component of heart", registry_identifier="fma0328405"),
            ],
        )
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "heart",
                "ontology": "fma",
                "type": "class",
                "rows": 20,
                "obsoletes": "false",
            },
            timeout=10,
        )
        mock_get.return_value.raise_for_status.assert_called_once_with()

    @patch("biodata_models.human_anatomy.requests.get")
    def test_search_by_name_exact_match(self, mock_get):
        """Exact search keeps case-insensitive label matches only."""
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "fma7088", "label": "Heart"},
                    {"obo_id": "fma0328405", "label": "Organ component of heart"},
                ]
            }
        }

        result = HumanAnatomy.search_by_name(" HEART ", exact_match=True)

        self.assertEqual(result, [HumanAnatomyModel(name="Heart", registry_identifier="fma7088")])

    @patch("biodata_models.human_anatomy.requests.get")
    def test_get_by_name_returns_exact_fma_term(self, mock_get):
        """Exact lookup creates a term model with the FMA registry."""
        mock_get.return_value.json.return_value = {
            "response": {"docs": [{"obo_id": "fma7088", "label": "Heart"}]}
        }

        result = HumanAnatomy.get_by_name("Heart")

        self.assertEqual(
            result,
            HumanAnatomyModel(name="Heart", registry=Registry.FMA, registry_identifier="fma7088"),
        )

    @patch("biodata_models.human_anatomy.requests.get")
    def test_get_by_name_returns_none_when_missing(self, mock_get):
        """Exact lookup returns None when no term is found."""
        mock_get.return_value.json.return_value = {"response": {"docs": []}}

        self.assertIsNone(HumanAnatomy.get_by_name("not an anatomy term"))

    @patch("biodata_models.human_anatomy.requests.get")
    def test_get_by_name_rejects_ambiguous_labels(self, mock_get):
        """Exact lookup rejects duplicate labels instead of choosing arbitrarily."""
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "fma1", "label": "Shared anatomy label"},
                    {"obo_id": "fma2", "label": "Shared anatomy label"},
                ]
            }
        }

        with self.assertRaises(ValueError):
            HumanAnatomy.get_by_name("Shared anatomy label")

    @patch("biodata_models.human_anatomy.requests.get")
    def test_search_by_name_rejects_empty_name_and_invalid_limit(self, mock_get):
        """Search rejects invalid inputs without issuing a request."""
        with self.assertRaises(ValueError):
            HumanAnatomy.search_by_name("  ")
        with self.assertRaises(ValueError):
            HumanAnatomy.search_by_name("heart", limit=101)

        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()