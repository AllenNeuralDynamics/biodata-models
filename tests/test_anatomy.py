"""Tests for shared anatomy models and OLS4 lookups."""

import unittest
from unittest.mock import patch

from biodata_models.anatomy import AnatomyModel, HumanAnatomy, MouseAnatomy
from biodata_models.registries import Registry


class AnatomyTests(unittest.TestCase):
    """Tests for the shared anatomy model and ontology searches."""

    def test_ontology_models_share_anatomy_base(self):
        """Mouse and human anatomy terms share a common model base."""
        self.assertTrue(issubclass(MouseAnatomy, AnatomyModel))
        self.assertTrue(issubclass(HumanAnatomy, AnatomyModel))

    def test_base_model_search_requires_ontology_configuration(self):
        """The shared base cannot search without an ontology configuration."""
        with self.assertRaisesRegex(NotImplementedError, "Use MouseAnatomy or HumanAnatomy"):
            AnatomyModel.search_by_name("heart")

    def test_anatomy_term_round_trips_json(self):
        """Ontology-specific anatomy models retain Pydantic serialization behavior."""
        model = MouseAnatomy(name="heart", registry_identifier="EMAPA:16105")

        round_trip = MouseAnatomy.model_validate_json(model.model_dump_json())

        self.assertEqual(model, round_trip)

    @patch("biodata_models.anatomy.requests.get")
    def test_mouse_search_by_name_uses_emapa(self, mock_get):
        """Mouse searches use EMAPA identifiers and discard unrelated or obsolete hits."""
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "EMAPA:16105", "label": "heart"},
                    {"obo_id": "DOID:123", "label": "heart disease"},
                    {"obo_id": "EMAPA:999", "label": "obsolete term", "is_obsolete": True},
                ]
            }
        }

        result = MouseAnatomy.search_by_name(" heart ")

        self.assertEqual(
            result,
            [MouseAnatomy(name="heart", registry_identifier="EMAPA:16105")],
        )
        self.assertIsInstance(result[0], AnatomyModel)
        self.assertEqual(result[0].registry, Registry.EMAPA)
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "heart",
                "ontology": "emapa",
                "type": "class",
                "rows": 50,
                "obsoletes": "false",
            },
            timeout=10,
        )

    @patch("biodata_models.anatomy.requests.get")
    def test_human_search_exact_match_uses_fma(self, mock_get):
        """Human exact search uses FMA and filters labels case-insensitively."""
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {"obo_id": "fma7088", "label": "Heart"},
                    {"obo_id": "fma0328405", "label": "Organ component of heart"},
                ]
            }
        }

        result = HumanAnatomy.search_by_name(" HEART ", exact_match=True)

        self.assertEqual(result, [HumanAnatomy(name="Heart", registry_identifier="fma7088")])
        self.assertEqual(result[0].registry, Registry.FMA)
        mock_get.assert_called_once_with(
            "https://www.ebi.ac.uk/ols4/api/search",
            params={
                "q": "HEART",
                "ontology": "fma",
                "type": "class",
                "rows": 50,
                "obsoletes": "false",
            },
            timeout=10,
        )

    @patch("biodata_models.anatomy.requests.get")
    def test_get_by_name_returns_exact_term_or_none(self, mock_get):
        """get_by_name returns an exact term and returns None when absent."""
        mock_get.return_value.json.return_value = {"response": {"docs": [{"obo_id": "EMAPA:16105", "label": "heart"}]}}

        self.assertEqual(
            MouseAnatomy.get_by_name("heart"),
            MouseAnatomy(name="heart", registry_identifier="EMAPA:16105"),
        )

        mock_get.return_value.json.return_value = {"response": {"docs": []}}
        self.assertIsNone(HumanAnatomy.get_by_name("not an anatomy term"))

    @patch("biodata_models.anatomy.requests.get")
    def test_get_by_name_rejects_ambiguous_labels(self, mock_get):
        """get_by_name does not choose arbitrarily between duplicate labels."""
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

    @patch("biodata_models.anatomy.requests.get")
    def test_search_rejects_invalid_inputs_without_request(self, mock_get):
        """Search input validation happens before making the HTTP request."""
        with self.assertRaises(ValueError):
            MouseAnatomy.search_by_name("  ")
        with self.assertRaises(ValueError):
            HumanAnatomy.search_by_name("heart", limit=101)

        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
