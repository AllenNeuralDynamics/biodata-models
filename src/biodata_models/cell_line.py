"""Cell Line Ontology lookup through OLS4."""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

OLS_SEARCH_URL = "https://www.ebi.ac.uk/ols4/api/search"


class CellLineModel(BaseModel):
    """Base model for a Cell Line Ontology term."""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry = Registry.CLO
    registry_identifier: str


class CellLine:
    """Search and resolve cell-line terms from the CLO ontology."""

    @classmethod
    def search_by_name(
        cls,
        name: str,
        *,
        exact_match: bool = False,
        limit: int = 10,
    ) -> list[CellLineModel]:
        """Search CLO terms by label using the public OLS4 API."""
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("name must not be empty")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        response = requests.get(
            OLS_SEARCH_URL,
            params={
                "q": normalized_name,
                "ontology": "clo",
                "type": "class",
                "rows": max(limit * 5, 20),
                "obsoletes": "false",
            },
            timeout=10,
        )
        response.raise_for_status()
        terms = response.json().get("response", {}).get("docs", []) or []

        cell_lines = []
        for term in terms:
            label = term.get("label")
            identifier = term.get("obo_id", "")
            if not label or not identifier.startswith("CLO:"):
                continue
            if term.get("is_obsolete", False):
                continue
            if exact_match and label.casefold() != normalized_name.casefold():
                continue

            cell_lines.append(
                CellLineModel(
                    name=label,
                    registry_identifier=identifier,
                )
            )
            if len(cell_lines) == limit:
                break

        return cell_lines

    @classmethod
    def get_by_name(cls, name: str) -> CellLineModel | None:
        """Return the unique exact-label CLO match, or None if no match exists."""
        matches = cls.search_by_name(name, exact_match=True, limit=2)
        if len(matches) > 1:
            raise ValueError(f"Multiple Cell Line Ontology terms have the exact label {name!r}")
        return matches[0] if matches else None
