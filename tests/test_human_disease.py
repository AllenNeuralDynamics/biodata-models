"""Tests for Human Disease Ontology lookup."""

import unittest
from unittest.mock import Mock, patch

from biodata_models.human_disease import HumanDisease, HumanDiseaseModel
from biodata_models.registries import Registry


class HumanDiseaseTests(unittest.TestCase):
    """Tests Human Disease Ontology lookup."""

    @patch("biodata_models.human_disease.requests.get")
    def test_search_by_name_returns_only_active_doid_terms(self, mock_get):
        """Search results exclude imported terms and obsolete diseases."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "DOID:10652", "label": "Alzheimer disease"},
                    {"obo_id": "CHEBI:102166", "label": "thiopental"},
                    {
                        "obo_id": "DOID:0110037",
                        "label": "Alzheimer disease 5",
                        "is_obsolete": True,
                    },
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanDisease.search_by_name(" Alzheimer ", limit=2)

        self.assertEqual(
            result,
            [
                HumanDiseaseModel(
                    name="Alzheimer disease",
                    registry=Registry.DOID,
                    registry_identifier="DOID:10652",
                )
            ],
        )
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "Alzheimer",
                "ontology": "doid",
                "type": "class",
                "rows": 20,
                "obsoletes": "false",
            },
            timeout=10,
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch("biodata_models.human_disease.requests.get")
    def test_search_by_name_exact_match(self, mock_get):
        """Exact mode filters by the case-insensitive primary label."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "DOID:1", "label": "Alzheimer disease"},
                    {"obo_id": "DOID:2", "label": "Alzheimer disease 2"},
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanDisease.search_by_name("ALZHEIMER DISEASE", exact_match=True)

        self.assertEqual([term.registry_identifier for term in result], ["DOID:1"])

    @patch("biodata_models.human_disease.requests.get")
    def test_get_by_name_returns_exact_doid_term(self, mock_get):
        """The class convenience method returns the exact disease model."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "DOID:1", "label": "Alzheimer disease"},
                    {"obo_id": "DOID:2", "label": "Alzheimer disease 2"},
                ]
            }
        }
        mock_get.return_value = mock_response

        result = HumanDisease.get_by_name("Alzheimer disease")

        self.assertEqual(
            result,
            HumanDiseaseModel(name="Alzheimer disease", registry_identifier="DOID:1"),
        )

    @patch("biodata_models.human_disease.requests.get")
    def test_get_by_name_returns_none_when_missing(self, mock_get):
        """The class convenience method returns None when no label matches."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": {"docs": []}}
        mock_get.return_value = mock_response

        self.assertIsNone(HumanDisease.get_by_name("not a disease"))

    @patch("biodata_models.human_disease.requests.get")
    def test_get_by_name_rejects_ambiguous_labels(self, mock_get):
        """The class method does not choose arbitrarily between duplicate labels."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "DOID:1", "label": "Shared disease label"},
                    {"obo_id": "DOID:2", "label": "Shared disease label"},
                ]
            }
        }
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            HumanDisease.get_by_name("Shared disease label")

    @patch("biodata_models.human_disease.requests.get")
    def test_search_by_name_rejects_empty_name_and_invalid_limit(self, mock_get):
        """Invalid search inputs fail before making a request."""
        with self.assertRaises(ValueError):
            HumanDisease.search_by_name(" ")
        with self.assertRaises(ValueError):
            HumanDisease.search_by_name("cancer", limit=101)

        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
