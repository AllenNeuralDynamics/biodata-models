"""Mouse and human anatomy ontology models backed by OLS4."""

from enum import Enum
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
            raise NotImplementedError("Use MouseAnatomyLookup or HumanAnatomyLookup for ontology lookups")

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


class MouseAnatomyLookup(AnatomyModel):
    """Search mouse anatomy terms from the EMAPA ontology."""

    registry: Registry = Registry.EMAPA
    _ontology: ClassVar[str] = "emapa"
    _identifier_prefix: ClassVar[str] = "EMAPA:"


class MouseEmgMuscles(str, Enum):
    """Mouse anatomy targets used for EMG muscles."""

    DELTOID = "deltoid"
    PECTORALIS_MAJOR = "pectoralis major"
    TRICEPS_BRACHII = "triceps brachii"
    LATERAL_HEAD_OF_TRICEPS_BRACHII = "lateral head of triceps brachii"
    LONG_HEAD_OF_TRICEPS_BRACHII = "long head of triceps brachii"
    MEDIAL_HEAD_OF_TRICEPS_BRACHII = "medial head of triceps brachii"
    BICEPS_BRACHII = "biceps brachii"
    LONG_HEAD_OF_BICEPS_BRACHII = "long head of biceps brachii"
    SHORT_HEAD_OF_BICEPS_BRACHII = "short head of biceps brachii"
    TENDON_OF_BICEPS_BRACHII = "tendon of biceps brachii"
    PARS_SCAPULARIS_OF_DELTOID = "pars scapularis of deltoid"
    EXTENSOR_CARPI_RADIALIS_LONGUS = "extensor carpi radialis longus"
    EXTENSOR_DIGITORUM_COMMUNIS = "extensor digitorum communis"
    EXTENSOR_DIGITORUM_LATERALIS = "extensor digitorum lateralis"
    EXTENSOR_CARPI_ULNARIS = "extensor carpi ulnaris"
    FLEXOR_CARPI_RADIALIS = "flexor carpi radialis"
    FLEXOR_CARPI_ULNARIS = "flexor carpi ulnaris"
    FLEXOR_DIGITORUM_PROFUNDUS = "flexor digitorum profundus"


class MouseBodyParts(str, Enum):
    """Mouse anatomy targets used for body parts."""

    FORELIMB = "forelimb"
    HEAD = "head"
    HINDLIMB = "hindlimb"
    NECK = "neck"
    TAIL = "tail"
    TRUNK = "trunk"


class MouseGroundWireLocations(str, Enum):
    """Mouse anatomy targets used for ground-wire locations."""

    FORELIMB = "forelimb"
    HEAD = "head"
    HINDLIMB = "hindlimb"
    NECK = "neck"
    TAIL = "tail"
    TRUNK = "trunk"
    BRAIN = "brain"
    CRANIUM = "cranium"


class MouseBloodVessels(str, Enum):
    """Mouse anatomy targets used for blood vessels."""

    CAROTID_ARTERY = "carotid artery"
    JUGULAR_VEIN = "jugular vein"


class MouseInjectionTargets(str, Enum):
    """Mouse anatomy targets used for common injection targets."""

    RETRO_ORBITAL = "venous sinus"
    INTRAPERITONEAL = "peritoneal cavity"


class HumanAnatomyLookup(AnatomyModel):
    """Search human anatomy terms from the Foundational Model of Anatomy."""

    registry: Registry = Registry.FMA
    _ontology: ClassVar[str] = "fma"
    _identifier_prefix: ClassVar[str] = "fma"
