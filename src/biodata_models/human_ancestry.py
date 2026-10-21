"""Human Ancestry Ontology lookup through OLS4."""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

OLS_SEARCH_URL = "https://www.ebi.ac.uk/ols4/api/search"


class HumanAncestryModel(BaseModel):
    """A human ancestry term from the Human Ancestry Ontology."""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry = Registry.HANCESTRO
    registry_identifier: str


class HumanAncestryLookup:
    """Search the Human Ancestry Ontology through OLS4."""

    @classmethod
    def search_by_name(
        cls,
        name: str,
        *,
        exact_match: bool = False,
        limit: int = 10,
    ) -> list[HumanAncestryModel]:
        """Return relevance-ranked HANCESTRO terms matching a name or synonym.

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
                "ontology": "hancestro",
                "type": "class",
                "rows": max(limit * 5, 20),
                "obsoletes": "false",
            },
            timeout=10,
        )
        response.raise_for_status()
        documents = response.json().get("response", {}).get("docs", []) or []

        terms = []
        for document in documents:
            identifier = document.get("obo_id", "")
            label = document.get("label")
            if not identifier.startswith("HANCESTRO:") or not label:
                continue
            if document.get("is_obsolete", False):
                continue
            if exact_match and label.casefold() != normalized_name.casefold():
                continue

            terms.append(
                HumanAncestryModel(
                    name=label,
                    registry_identifier=identifier,
                )
            )
            if len(terms) == limit:
                break

        return terms

    @classmethod
    def get_by_name(cls, name: str) -> HumanAncestryModel | None:
        """Return the uniquely labeled HANCESTRO term, or None when no exact label matches."""
        matches = cls.search_by_name(name, exact_match=True, limit=2)
        if len(matches) > 1:
            raise ValueError(f"Multiple Human Ancestry Ontology terms have the exact label {name!r}")
        return matches[0] if matches else None
