"""Tests classes with fixed Literal values match defaults"""

import unittest

from pydantic import BaseModel

from biodata_models.harp_types import HarpDeviceType
from biodata_models.organizations import Organization
from biodata_models.species import Species
from biodata_models.mouse_anatomy import MouseAnatomy, MouseAnatomyModel, MouseEmgMuscles
from biodata_models.mouse_developmental_stage import MouseDevelopmentalStage
from biodata_models.human_developmental_stage import HumanDevelopmentalStage
from biodata_models.drosophila_developmental_stage import DrosophilaDevelopmentalStage
from biodata_models.celegans_developmental_stage import CElegansDevelopmentalStage
from biodata_models.protocols import Protocols


class LiteralAndDefaultTests(unittest.TestCase):
    """Tests Literals match defaults in several classes"""

    def test_organizations(self):
        """Test Literals match defaults"""

        for organization in Organization.ALL:
            model = organization()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_harp(self):
        """Test Literals match defaults"""

        for harp in HarpDeviceType.ALL:
            model = harp()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_species(self):
        """Test Literals match defaults"""

        for species in Species.ALL:
            model = species()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_mouse_anatomy(self):
        """Test Literals match defaults"""
        structures = [
            "ANATOMICAL_STRUCTURE",
            "FIRST_POLAR_BODY",
            "_1_CELL_STAGE_EMBRYO",
            "SECOND_POLAR_BODY",
            "ZONA_PELLUCIDA",
            "_2_CELL_STAGE_EMBRYO",
        ]

        for structure in structures:
            model = getattr(MouseAnatomy, structure)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_mouse_developmental_stage(self):
        """Test Literals match defaults"""
        stages = ["LIFE_CYCLE_STAGE", "YOUNG_ADULT_STAGE", "LATE_ADULT_STAGE"]

        for stage in stages:
            model = getattr(MouseDevelopmentalStage, stage)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_human_developmental_stage(self):
        """Test Literals match defaults"""
        stages = ["ADULT_STAGE", "LATE_ADULT_STAGE", "PRIME_ADULT_STAGE"]

        for stage in stages:
            model = getattr(HumanDevelopmentalStage, stage)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_drosophila_developmental_stage(self):
        """Test Literals match defaults"""
        stages = ["ADULT_STAGE", "ADULT_AGE_IN_DAYS"]

        for stage in stages:
            model = getattr(DrosophilaDevelopmentalStage, stage)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_celegans_developmental_stage(self):
        """Test Literals match defaults"""
        stages = ["C__ELEGANS_LIFE_STAGE"]

        for stage in stages:
            model = getattr(CElegansDevelopmentalStage, stage)
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)
            self.assertEqual(model, round_trip)

    def test_mouse_custom_features(self):
        """Test that the custom __getattribute__ functionality works properly"""
        # ensure that class methods still return properly and don't trigger the custom __getattribute__ functionality
        self.assertIsNotNone(MouseAnatomy.__module__)
        self.assertIsNotNone(MouseAnatomy.__dict__)

        # generate a model from the class
        class TestModel(BaseModel):
            """test class"""

            structure: MouseAnatomyModel = MouseAnatomy.ANATOMICAL_STRUCTURE

        test = TestModel()
        self.assertIsNotNone(test)

        # generate a test model using the emg group
        class TestModel2(BaseModel):
            """test class"""

            structure: MouseAnatomyModel = MouseEmgMuscles.DELTOID

        test = TestModel2()
        self.assertIsNotNone(test)

    def test_protocols_instantiation(self):
        """Test that Protocols can be instantiated and have correct names"""
        self.assertIsNotNone(Protocols.SOLENOID_VALVE_CALIBRATION_FOR_BEHAVIOR_RIGS_UTILIZING_WATER_REWARD_V1)
        self.assertEqual(
            Protocols.SOLENOID_VALVE_CALIBRATION_FOR_BEHAVIOR_RIGS_UTILIZING_WATER_REWARD_V1.name,
            "Solenoid Valve Calibration for Behavior Rigs Utilizing Water Reward",
        )
        self.assertEqual(
            Protocols.SOLENOID_VALVE_CALIBRATION_FOR_BEHAVIOR_RIGS_UTILIZING_WATER_REWARD_V1.version,
            1,
        )


if __name__ == "__main__":
    unittest.main()
