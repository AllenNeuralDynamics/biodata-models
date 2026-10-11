"""Tests for data level and collection group vocabularies."""

import unittest

from biodata_models.data_name_patterns import DataLevel, Group


class TestDataNameVocabularies(unittest.TestCase):
    """Tests for the vocabularies retained in biodata-models."""

    def test_data_levels(self):
        """Test the supported data levels."""
        self.assertEqual({"derived", "raw", "simulated"}, {level.value for level in DataLevel})

    def test_groups(self):
        """Test the supported data collection groups."""
        self.assertEqual({"behavior", "ephys", "MSMA", "ophys", "NBA"}, {group.value for group in Group})
