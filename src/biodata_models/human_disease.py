"""Human Disease Ontology lookup through OLS4."""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

OLS_SEARCH_URL = "https://www.ebi.ac.uk/ols4/api/search"


class HumanDiseaseModel(BaseModel):
    """A human disease term from the Disease Ontology."""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry = Registry.DOID
    registry_identifier: str


class HumanDisease:
    """Search the Human Disease Ontology through OLS4."""

    @classmethod
    def search_by_name(
        cls,
        name: str,
        *,
        exact_match: bool = False,
        limit: int = 10,
    ) -> list[HumanDiseaseModel]:
        """Return relevance-ranked DOID terms matching a name or synonym.

        OLS4's full-text search is ranked but does not correct misspellings.
        When ``exact_match`` is true, only case-insensitive label matches are returned.
        """
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("name must not be empty")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        response = requests.get(
            OLS_SEARCH_URL,
            params={
                "q": normalized_name,
                "ontology": "doid",
                "type": "class",
                "rows": max(limit * 5, 20),
                "obsoletes": "false",
            },
            timeout=10,
        )
        response.raise_for_status()
        documents = response.json().get("response", {}).get("docs", []) or []

        diseases = []
        for document in documents:
            identifier = document.get("obo_id", "")
            label = document.get("label")
            if not identifier.startswith("DOID:") or not label:
                continue
            if document.get("is_obsolete", False):
                continue
            if exact_match and label.casefold() != normalized_name.casefold():
                continue

            diseases.append(
                HumanDiseaseModel(
                    name=label,
                    registry_identifier=identifier,
                )
            )
            if len(diseases) == limit:
                break

        return diseases

    @classmethod
    def get_by_name(cls, name: str) -> HumanDiseaseModel | None:
        """Return the uniquely labeled DOID term, or None when no exact label matches."""
        matches = cls.search_by_name(name, exact_match=True, limit=2)
        if len(matches) > 1:
            raise ValueError(f"Multiple Disease Ontology terms have the exact label {name!r}")
        return matches[0] if matches else None
