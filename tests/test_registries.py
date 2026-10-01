"""Tests classes in registries module"""

import unittest

from biodata_models.registries import Registry


class TestRegistry(unittest.TestCase):
    """Tests methods in Registry class"""

    def test_class_construction(self):
        """Tests enum can be instantiated via string"""

        self.assertEqual(Registry.ADDGENE, "Addgene (ADDGENE)")

    def test_ols_ontology_registry_values(self):
        """Tests registries required by OLS ontology lookups are available."""
        self.assertEqual(Registry.DOID, "Human Disease Ontology (DOID)")
        self.assertEqual(Registry.CLO, "Cell Line Ontology (CLO)")
        self.assertEqual(Registry.FMA, "Foundational Model of Anatomy (FMA)")


if __name__ == "__main__":
    unittest.main()
