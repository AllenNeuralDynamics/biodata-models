"""Mouse and human anatomy ontology models backed by OLS4."""

from typing import ClassVar, TypeVar

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

OLS_SEARCH_URL = "https://www.ebi.ac.uk/ols4/api/search"
AnatomyType = TypeVar("AnatomyType", bound="AnatomyModel")


class AnatomyModel(BaseModel):
    """Shared model for anatomy terms from different ontologies."""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry
    registry_identifier: str

    _ontology: ClassVar[str] = ""
    _identifier_prefix: ClassVar[str] = ""

    @classmethod
    def search_by_name(
        cls: type[AnatomyType],
        name: str,
        *,
        exact_match: bool = False,
        limit: int = 10,
    ) -> list[AnatomyType]:
        """Return relevance-ranked terms matching a name or synonym.

        OLS4's full-text search is ranked but does not correct misspellings.
        When ``exact_match`` is true, only case-insensitive label matches are returned.
        """
        if not cls._ontology or not cls._identifier_prefix:
            raise NotImplementedError("Use MouseAnatomy or HumanAnatomy for ontology lookups")

        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("name must not be empty")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        response = requests.get(
            OLS_SEARCH_URL,
            params={
                "q": normalized_name,
                "ontology": cls._ontology,
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
            if (
                not isinstance(identifier, str)
                or not identifier.casefold().startswith(cls._identifier_prefix.casefold())
                or not isinstance(label, str)
                or not label
            ):
                continue
            if document.get("is_obsolete", False):
                continue
            if exact_match and label.casefold() != normalized_name.casefold():
                continue

            terms.append(cls(name=label, registry_identifier=identifier))
            if len(terms) == limit:
                break

        return terms

    @classmethod
    def get_by_name(cls: type[AnatomyType], name: str) -> AnatomyType | None:
        """Return the uniquely labeled term, or None when no exact label matches."""
        matches = cls.search_by_name(name, exact_match=True, limit=2)
        if len(matches) > 1:
            raise ValueError(f"Multiple {cls._ontology.upper()} anatomy terms have the exact label {name!r}")
        return matches[0] if matches else None


class MouseAnatomy(AnatomyModel):
    """Search mouse anatomy terms from the EMAPA ontology."""

    registry: Registry = Registry.EMAPA
    _ontology: ClassVar[str] = "emapa"
    _identifier_prefix: ClassVar[str] = "EMAPA:"


class HumanAnatomy(AnatomyModel):
    """Search human anatomy terms from the Foundational Model of Anatomy."""

    registry: Registry = Registry.FMA
    _ontology: ClassVar[str] = "fma"
    _identifier_prefix: ClassVar[str] = "fma"
