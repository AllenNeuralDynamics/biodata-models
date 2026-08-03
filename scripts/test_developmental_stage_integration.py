"""Integration test for developmental stage ontology lookups (MMUSDV, HSAPDV, FBDV, WBLS)."""

import sys

from biodata_models.mouse_developmental_stage import MouseDevelopmentalStage
from biodata_models.human_developmental_stage import HumanDevelopmentalStage
from biodata_models.drosophila_developmental_stage import DrosophilaDevelopmentalStage
from biodata_models.celegans_developmental_stage import CElegansDevelopmentalStage


def check(label, model, expected_name, expected_registry):
    """Check that a resolved model has the expected name/registry and a non-empty identifier"""
    print(f"{label}: name={model.name}, registry={model.registry}, registry_identifier={model.registry_identifier}")
    assert model.name.lower() == expected_name.lower()
    assert model.registry.name == expected_registry
    assert model.registry_identifier is not None and model.registry_identifier != ""


def main():
    """Main function to test developmental stage ontology integrations"""
    try:
        check("MouseDevelopmentalStage.LIFE_CYCLE_STAGE", MouseDevelopmentalStage.LIFE_CYCLE_STAGE, "life cycle stage", "MMUSDV")
        check("HumanDevelopmentalStage.ADULT_STAGE", HumanDevelopmentalStage.ADULT_STAGE, "adult stage", "HSAPDV")
        check("DrosophilaDevelopmentalStage.ADULT_STAGE", DrosophilaDevelopmentalStage.ADULT_STAGE, "adult stage", "FBDV")
        check(
            "CElegansDevelopmentalStage.C__ELEGANS_LIFE_STAGE",
            CElegansDevelopmentalStage.C__ELEGANS_LIFE_STAGE,
            "C. elegans life stage",
            "WBLS",
        )
        print("Developmental stage ontology integration test passed.")
    except Exception as e:
        print(f"Developmental stage ontology integration test failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
