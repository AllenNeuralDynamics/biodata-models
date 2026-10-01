"""Integration test for MouseAnatomyLookup model EMAPA lookup."""

import sys
from biodata_models.anatomy import MouseAnatomyLookup


def main():
    """Main function to test MouseAnatomyLookup integration"""
    try:
        heart = MouseAnatomyLookup.get_by_name("heart")
        if heart is None:
            raise ValueError("Could not find the mouse anatomy term 'heart'")
        print(
            f"MouseAnatomyLookup.get_by_name('heart'): name={heart.name}, registry={heart.registry}"
            f", registry_identifier={heart.registry_identifier}"
        )
        assert heart.name.lower() == "heart"
        assert heart.registry.name == "EMAPA"
        assert heart.registry_identifier is not None and heart.registry_identifier != ""
        print("MouseAnatomyLookup integration test passed.")
    except Exception as e:
        print(f"MouseAnatomyLookup integration test failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
