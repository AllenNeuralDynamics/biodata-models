"""Tests for the data level vocabulary."""

import unittest

from biodata_models.data_levels import DataLevel


class TestDataNameVocabularies(unittest.TestCase):
    """Tests for the vocabularies retained in biodata-models."""

    def test_data_levels(self):
        """Test the supported data levels."""
        self.assertEqual({"derived", "raw", "simulated"}, {level.value for level in DataLevel})
