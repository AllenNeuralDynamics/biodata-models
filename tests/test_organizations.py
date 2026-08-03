"""Tests classes in organizations module"""

import unittest

from biodata_models.organizations import Organization


class TestOrganization(unittest.TestCase):
    """Tests methods in Organization class"""

    def test_name_map(self):
        """Tests Organization name_map property"""

        self.assertEqual(Organization.AI, Organization.name_map["Allen Institute"])

    def test_none(self):
        """Tests that empty strings map to None"""

        self.assertEqual(Organization.LIFECANVAS.abbreviation, None)

    def test_from_none(self):
        """Test that you can't get an organization from None"""

        self.assertEqual(Organization.from_abbreviation(None), None)


if __name__ == "__main__":
    unittest.main()
