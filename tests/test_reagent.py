"""Test reagent enums"""

import unittest

from biodata_models.reagent import FluorophoreType


class UnitsTests(unittest.TestCase):
    """Class for testing reagent enums"""

    def test_units(self):
        """Tests creation of a FluorophoreType object"""

        self.assertIsNotNone(FluorophoreType.ALEXA)


if __name__ == "__main__":
    unittest.main()
