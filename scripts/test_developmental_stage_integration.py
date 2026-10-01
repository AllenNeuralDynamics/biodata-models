"""Integration test for developmental stage ontology lookups (MMUSDV, HSAPDV, FBDV, WBLS)."""

import sys

from biodata_models.mouse_developmental_stage import MouseDevelopmentalStageLookup
from biodata_models.human_developmental_stage import HumanDevelopmentalStageLookup
from biodata_models.drosophila_developmental_stage import DrosophilaDevelopmentalStageLookup
from biodata_models.celegans_developmental_stage import CElegansDevelopmentalStageLookup


def check(label, model, expected_name, expected_registry):
    """Check that a resolved model has the expected name/registry and a non-empty identifier"""
    print(f"{label}: name={model.name}, registry={model.registry}, registry_identifier={model.registry_identifier}")
    assert model.name.lower() == expected_name.lower()
    assert model.registry.name == expected_registry
    assert model.registry_identifier is not None and model.registry_identifier != ""


def main():
    """Main function to test developmental stage ontology integrations"""
    try:
        check(
            "MouseDevelopmentalStageLookup.LIFE_CYCLE_STAGE",
            MouseDevelopmentalStageLookup.LIFE_CYCLE_STAGE,
            "life cycle stage",
            "MMUSDV"
        )
        check(
            "HumanDevelopmentalStageLookup.ADULT_STAGE",
            HumanDevelopmentalStageLookup.ADULT_STAGE,
            "adult stage",
            "HSAPDV"
        )
        check(
            "DrosophilaDevelopmentalStageLookup.ADULT_STAGE",
            DrosophilaDevelopmentalStageLookup.ADULT_STAGE,
            "adult stage",
            "FBDV"
        )
        check(
            "CElegansDevelopmentalStageLookup.C__ELEGANS_LIFE_STAGE",
            CElegansDevelopmentalStageLookup.C__ELEGANS_LIFE_STAGE,
            "C. elegans life stage",
            "WBLS",
        )
        print("Developmental stage ontology integration test passed.")
    except Exception as e:
        print(f"Developmental stage ontology integration test failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
