"""Tests for Human Ancestry Ontology lookup."""

import unittest
from unittest.mock import Mock, patch

from biodata_models.human_ancestry import HumanAncestryLookup, HumanAncestryModel
from biodata_models.registries import Registry


class HumanAncestryTests(unittest.TestCase):
    """Tests Human Ancestry Ontology lookup."""

    @patch("biodata_models.human_ancestry.requests.get")
    def test_search_by_name_returns_only_active_hancestro_terms(self, mock_get):
        """Search results exclude imported terms and obsolete ancestry terms."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "HANCESTRO:0005", "label": "European ancestry"},
                    {"obo_id": "NCBITaxon:9606", "label": "Homo sapiens"},
                    {
                        "obo_id": "HANCESTRO:0001",
                        "label": "Obsolete ancestry",
                        "is_obsolete": True,
                    },
                    {"obo_id": "HANCESTRO:0002"},
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanAncestryLookup.search_by_name(" European ", limit=2)

        self.assertEqual(
            result,
            [
                HumanAncestryModel(
                    name="European ancestry",
                    registry=Registry.HANCESTRO,
                    registry_identifier="HANCESTRO:0005",
                )
            ],
        )
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "European",
                "ontology": "hancestro",
                "type": "class",
                "rows": 20,
                "obsoletes": "false",
            },
            timeout=10,
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch("biodata_models.human_ancestry.requests.get")
    def test_search_by_name_exact_match(self, mock_get):
        """Exact mode filters by the case-insensitive primary label."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "HANCESTRO:0005", "label": "European ancestry"},
                    {"obo_id": "HANCESTRO:0590", "label": "European American"},
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanAncestryLookup.search_by_name("EUROPEAN ANCESTRY", exact_match=True)

        self.assertEqual([term.registry_identifier for term in result], ["HANCESTRO:0005"])

    @patch("biodata_models.human_ancestry.requests.get")
    def test_get_by_name_returns_exact_term(self, mock_get):
        """The class convenience method returns the exact ancestry model."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "HANCESTRO:0005", "label": "European ancestry"},
                    {"obo_id": "HANCESTRO:0590", "label": "European American"},
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanAncestryLookup.get_by_name("European ancestry")

        self.assertEqual(
            result,
            HumanAncestryModel(name="European ancestry", registry_identifier="HANCESTRO:0005"),
        )

    @patch("biodata_models.human_ancestry.requests.get")
    def test_get_by_name_returns_none_when_missing(self, mock_get):
        """The class convenience method returns None when no label matches."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": {"docs": []}}
        mock_get.return_value = mock_response

        self.assertIsNone(HumanAncestryLookup.get_by_name("not an ancestry"))

    @patch("biodata_models.human_ancestry.requests.get")
    def test_get_by_name_rejects_ambiguous_labels(self, mock_get):
        """The class method does not choose arbitrarily between duplicate labels."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "HANCESTRO:1", "label": "Shared label"},
                    {"obo_id": "HANCESTRO:2", "label": "Shared label"},
                ]
            }
        }
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            HumanAncestryLookup.get_by_name("Shared label")

    @patch("biodata_models.human_ancestry.requests.get")
    def test_search_by_name_rejects_empty_name_and_invalid_limit(self, mock_get):
        """Invalid search inputs fail before making a request."""
        with self.assertRaises(ValueError):
            HumanAncestryLookup.search_by_name(" ")
        with self.assertRaises(ValueError):
            HumanAncestryLookup.search_by_name("european", limit=101)

        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
