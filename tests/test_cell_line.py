"""Tests for OLS4-backed Cell Line Ontology lookups."""

import unittest
from unittest.mock import patch

from biodata_models.cell_line import CellLine, CellLineModel
from biodata_models.registries import Registry


class CellLineTests(unittest.TestCase):
    """Tests Cell Line Ontology searches and lookups."""

    @patch("biodata_models.cell_line.requests.get")
    def test_search_by_name_returns_active_clo_terms(self, mock_get):
        response = mock_get.return_value
        response.json.return_value = {
            "response": {
                "docs": [
                    {
                        "label": "HeLa cell",
                        "obo_id": "CLO:0000001",
                        "is_obsolete": False,
                    },
                    {
                        "label": "Imported cell",
                        "obo_id": "CL:0000001",
                        "is_obsolete": False,
                    },
                    {
                        "label": "Obsolete cell line",
                        "obo_id": "CLO:0000002",
                        "is_obsolete": True,
                    },
                ]
            }
        }

        result = CellLine.search_by_name(" HeLa ")

        self.assertEqual(
            result,
            [
                CellLineModel(
                    name="HeLa cell",
                    registry=Registry.CLO,
                    registry_identifier="CLO:0000001",
                )
            ],
        )
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "HeLa",
                "ontology": "clo",
                "type": "class",
                "rows": 50,
                "obsoletes": "false",
            },
            timeout=10,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("biodata_models.cell_line.requests.get")
    def test_search_by_name_exact_match(self, mock_get):
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"label": "HeLa cell", "obo_id": "CLO:0000001"},
                    {"label": "HeLa", "obo_id": "CLO:0000002"},
                ]
            }
        }

        result = CellLine.search_by_name("hela", exact_match=True)

        self.assertEqual([term.name for term in result], ["HeLa"])
        self.assertEqual(result[0].registry_identifier, "CLO:0000002")

    @patch("biodata_models.cell_line.requests.get")
    def test_search_by_name_ignores_terms_without_clo_identifier(self, mock_get):
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"label": "Cell", "obo_id": "CL:0000001"},
                    {"label": "Example cell line", "obo_id": "CLO:0000123"},
                ]
            }
        }

        result = CellLine.search_by_name("Example cell line")

        self.assertEqual(result[0].registry_identifier, "CLO:0000123")

    @patch("biodata_models.cell_line.CellLine.search_by_name")
    def test_get_by_name_returns_exact_term(self, mock_search):
        expected = CellLineModel(name="HeLa", registry_identifier="CLO:0000001")
        mock_search.return_value = [expected]

        self.assertEqual(CellLine.get_by_name("HeLa"), expected)
        mock_search.assert_called_once_with("HeLa", exact_match=True, limit=2)

    @patch("biodata_models.cell_line.CellLine.search_by_name", return_value=[])
    def test_get_by_name_returns_none_when_missing(self, _mock_search):
        self.assertIsNone(CellLine.get_by_name("Missing cell line"))

    @patch(
        "biodata_models.cell_line.CellLine.search_by_name",
        return_value=[
            CellLineModel(name="Duplicate", registry_identifier="CLO:0000001"),
            CellLineModel(name="Duplicate", registry_identifier="CLO:0000002"),
        ],
    )
    def test_get_by_name_rejects_ambiguous_labels(self, _mock_search):
        with self.assertRaisesRegex(ValueError, "Multiple Cell Line Ontology terms"):
            CellLine.get_by_name("Duplicate")

    @patch("biodata_models.cell_line.requests.get")
    def test_search_by_name_rejects_invalid_input(self, mock_get):
        with self.assertRaisesRegex(ValueError, "name must not be empty"):
            CellLine.search_by_name("  ")
        with self.assertRaisesRegex(ValueError, "limit must be between 1 and 100"):
            CellLine.search_by_name("HeLa", limit=101)
        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
