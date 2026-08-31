"""Drosophila developmental stage"""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

"""Drosophila developmental stage"""


class DrosophilaDevelopmentalStageModel(BaseModel):
    """Base model for drosophila developmental stage"""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry
    registry_identifier: str


def search_fbdv_exact_match(class_name):
    """Pull the exact name match from the FBDV ontology

    Parameters
    ----------
    class_name : str
        Name of class

    Returns
    -------
    list

    Raises
    ------
    Exception
        OLS query failed on any status code other than 200
    """
    base_url = "https://www.ebi.ac.uk/ols4/api/search"
    params = {
        "q": class_name,
        "ontology": "fbdv",  # Specify the ontology
        "type": "class",  # Search for classes
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Extract terms with exact label match
        exact_matches = [
            {
                "iri": entry["iri"],
                "label": entry["label"],
            }
            for entry in results.get("response", {}).get("docs", [])
            if entry["label"].lower() == class_name.lower()
        ]
        return exact_matches
    else:
        raise Exception(f"OLS query failed: {response.status_code}, {response.text}")


def get_fbdv_id(class_name):
    """Get the FBDV ID for a given class name

    Parameters
    ----------
    class_name : str

    Returns
    -------
    int
    """
    results = search_fbdv_exact_match(class_name)

    if results:
        return results[0]["iri"].split("_")[1]
    else:
        return None


class DrosophilaDevelopmentalStageMeta(type):
    """Meta class for DrosophilaDevelopmentalStage groups"""

    def __getattribute__(cls, name):
        """Custom get attribute function, validates developmental stage names against external FBDV registry

        Parameters
        ----------
        name : str
            Attribute name

        Raises
        ------
        ValueError
            Name not found in the FBDV registry
        """

        # bypass
        if name.startswith("__"):
            return object.__getattribute__(cls, name)

        class_dict = object.__getattribute__(cls, "__dict__")

        if name in class_dict:
            original_name = super().__getattribute__(name)

            fbdv_id = get_fbdv_id(original_name)

            if fbdv_id:
                return DrosophilaDevelopmentalStageModel(
                    name=original_name,
                    registry=Registry.FBDV,
                    registry_identifier=fbdv_id,
                )
            else:
                raise ValueError(f"Could not find FBDV ID for {original_name}")

        # second bypass for defined values
        return super().__getattribute__(name)


class DrosophilaDevelopmentalStage(metaclass=DrosophilaDevelopmentalStageMeta):
    """Drosophila developmental stage"""

    DROSOPHILA_LIFE = "Drosophila life"
    P_STAGE = "P-stage"
    ADULT_AGE_IN_DAYS = "adult age in days"
    ADULT_STAGE = "adult stage"
    ADULT_STAGE_A1 = "adult stage A1"
    ADULT_STAGE_A2 = "adult stage A2"
    ADULT_STAGE_A3 = "adult stage A3"
    AGE = "age"
    BIOLOGICAL_PROCESS = "biological process"
    BLASTODERM_STAGE = "blastoderm stage"
    CLEAVAGE_STAGE = "cleavage stage"
    DAY_0_OF_ADULTHOOD = "day 0 of adulthood"
    DAY_1_OF_ADULTHOOD = "day 1 of adulthood"
    DAY_10_OF_ADULTHOOD = "day 10 of adulthood"
    DAY_11_OF_ADULTHOOD = "day 11 of adulthood"
    DAY_12_OF_ADULTHOOD = "day 12 of adulthood"
    DAY_13_OF_ADULTHOOD = "day 13 of adulthood"
    DAY_14_OF_ADULTHOOD = "day 14 of adulthood"
    DAY_15_OF_ADULTHOOD = "day 15 of adulthood"
    DAY_16_OF_ADULTHOOD = "day 16 of adulthood"
    DAY_17_OF_ADULTHOOD = "day 17 of adulthood"
    DAY_18_OF_ADULTHOOD = "day 18 of adulthood"
    DAY_19_OF_ADULTHOOD = "day 19 of adulthood"
    DAY_2_OF_ADULTHOOD = "day 2 of adulthood"
    DAY_20_OF_ADULTHOOD = "day 20 of adulthood"
    DAY_21_OF_ADULTHOOD = "day 21 of adulthood"
    DAY_22_OF_ADULTHOOD = "day 22 of adulthood"
    DAY_23_OF_ADULTHOOD = "day 23 of adulthood"
    DAY_24_OF_ADULTHOOD = "day 24 of adulthood"
    DAY_25_OF_ADULTHOOD = "day 25 of adulthood"
    DAY_26_OF_ADULTHOOD = "day 26 of adulthood"
    DAY_27_OF_ADULTHOOD = "day 27 of adulthood"
    DAY_28_OF_ADULTHOOD = "day 28 of adulthood"
    DAY_29_OF_ADULTHOOD = "day 29 of adulthood"
    DAY_3_OF_ADULTHOOD = "day 3 of adulthood"
    DAY_30_OF_ADULTHOOD = "day 30 of adulthood"
    DAY_31_OF_ADULTHOOD = "day 31 of adulthood"
    DAY_32_OF_ADULTHOOD = "day 32 of adulthood"
    DAY_33_OF_ADULTHOOD = "day 33 of adulthood"
    DAY_34_OF_ADULTHOOD = "day 34 of adulthood"
    DAY_35_OF_ADULTHOOD = "day 35 of adulthood"
    DAY_36_OF_ADULTHOOD = "day 36 of adulthood"
    DAY_37_OF_ADULTHOOD = "day 37 of adulthood"
    DAY_38_OF_ADULTHOOD = "day 38 of adulthood"
    DAY_39_OF_ADULTHOOD = "day 39 of adulthood"
    DAY_4_OF_ADULTHOOD = "day 4 of adulthood"
    DAY_40_OF_ADULTHOOD = "day 40 of adulthood"
    DAY_41_OF_ADULTHOOD = "day 41 of adulthood"
    DAY_42_OF_ADULTHOOD = "day 42 of adulthood"
    DAY_43_OF_ADULTHOOD = "day 43 of adulthood"
    DAY_44_OF_ADULTHOOD = "day 44 of adulthood"
    DAY_45_OF_ADULTHOOD = "day 45 of adulthood"
    DAY_46_OF_ADULTHOOD = "day 46 of adulthood"
    DAY_47_OF_ADULTHOOD = "day 47 of adulthood"
    DAY_48_OF_ADULTHOOD = "day 48 of adulthood"
    DAY_49_OF_ADULTHOOD = "day 49 of adulthood"
    DAY_5_OF_ADULTHOOD = "day 5 of adulthood"
    DAY_50_OF_ADULTHOOD = "day 50 of adulthood"
    DAY_51_OF_ADULTHOOD = "day 51 of adulthood"
    DAY_52_OF_ADULTHOOD = "day 52 of adulthood"
    DAY_53_OF_ADULTHOOD = "day 53 of adulthood"
    DAY_54_OF_ADULTHOOD = "day 54 of adulthood"
    DAY_55_OF_ADULTHOOD = "day 55 of adulthood"
    DAY_56_OF_ADULTHOOD = "day 56 of adulthood"
    DAY_57_OF_ADULTHOOD = "day 57 of adulthood"
    DAY_58_OF_ADULTHOOD = "day 58 of adulthood"
    DAY_59_OF_ADULTHOOD = "day 59 of adulthood"
    DAY_6_OF_ADULTHOOD = "day 6 of adulthood"
    DAY_60_OF_ADULTHOOD = "day 60 of adulthood"
    DAY_61_OF_ADULTHOOD = "day 61 of adulthood"
    DAY_62_OF_ADULTHOOD = "day 62 of adulthood"
    DAY_63_OF_ADULTHOOD = "day 63 of adulthood"
    DAY_64_OF_ADULTHOOD = "day 64 of adulthood"
    DAY_65_OF_ADULTHOOD = "day 65 of adulthood"
    DAY_66_OF_ADULTHOOD = "day 66 of adulthood"
    DAY_67_OF_ADULTHOOD = "day 67 of adulthood"
    DAY_68_OF_ADULTHOOD = "day 68 of adulthood"
    DAY_69_OF_ADULTHOOD = "day 69 of adulthood"
    DAY_7_OF_ADULTHOOD = "day 7 of adulthood"
    DAY_70_OF_ADULTHOOD = "day 70 of adulthood"
    DAY_8_OF_ADULTHOOD = "day 8 of adulthood"
    DAY_9_OF_ADULTHOOD = "day 9 of adulthood"
    DEVELOPMENTAL_PROCESS = "developmental process"
    DEVELOPMENTAL_STAGE = "developmental stage"
    DORSAL_CLOSURE_STAGE = "dorsal closure stage"
    EARLY_EXTENDED_GERM_BAND_STAGE = "early extended germ band stage"
    EARLY_THIRD_INSTAR_LARVAL_STAGE = "early third instar larval stage"
    EGG_STAGE = "egg stage"
    EMBRYONIC_CYCLE = "embryonic cycle"
    EMBRYONIC_CYCLE_1 = "embryonic cycle 1"
    EMBRYONIC_CYCLE_10 = "embryonic cycle 10"
    EMBRYONIC_CYCLE_11 = "embryonic cycle 11"
    EMBRYONIC_CYCLE_12 = "embryonic cycle 12"
    EMBRYONIC_CYCLE_13 = "embryonic cycle 13"
    EMBRYONIC_CYCLE_14 = "embryonic cycle 14"
    EMBRYONIC_CYCLE_14A = "embryonic cycle 14A"
    EMBRYONIC_CYCLE_14B = "embryonic cycle 14B"
    EMBRYONIC_CYCLE_15 = "embryonic cycle 15"
    EMBRYONIC_CYCLE_16 = "embryonic cycle 16"
    EMBRYONIC_CYCLE_2 = "embryonic cycle 2"
    EMBRYONIC_CYCLE_3 = "embryonic cycle 3"
    EMBRYONIC_CYCLE_4 = "embryonic cycle 4"
    EMBRYONIC_CYCLE_5 = "embryonic cycle 5"
    EMBRYONIC_CYCLE_6 = "embryonic cycle 6"
    EMBRYONIC_CYCLE_7 = "embryonic cycle 7"
    EMBRYONIC_CYCLE_8 = "embryonic cycle 8"
    EMBRYONIC_CYCLE_9 = "embryonic cycle 9"
    EMBRYONIC_CYCLE_M_PHASE = "embryonic cycle M-phase"
    EMBRYONIC_CYCLE_INTERPHASE = "embryonic cycle interphase"
    EMBRYONIC_STAGE = "embryonic stage"
    EMBRYONIC_STAGE_1 = "embryonic stage 1"
    EMBRYONIC_STAGE_10 = "embryonic stage 10"
    EMBRYONIC_STAGE_11 = "embryonic stage 11"
    EMBRYONIC_STAGE_12 = "embryonic stage 12"
    EMBRYONIC_STAGE_13 = "embryonic stage 13"
    EMBRYONIC_STAGE_14 = "embryonic stage 14"
    EMBRYONIC_STAGE_15 = "embryonic stage 15"
    EMBRYONIC_STAGE_16 = "embryonic stage 16"
    EMBRYONIC_STAGE_17 = "embryonic stage 17"
    EMBRYONIC_STAGE_17_I_ = "embryonic stage 17(i)"
    EMBRYONIC_STAGE_17_II_ = "embryonic stage 17(ii)"
    EMBRYONIC_STAGE_17_III_ = "embryonic stage 17(iii)"
    EMBRYONIC_STAGE_17_IV_ = "embryonic stage 17(iv)"
    EMBRYONIC_STAGE_2 = "embryonic stage 2"
    EMBRYONIC_STAGE_3 = "embryonic stage 3"
    EMBRYONIC_STAGE_4 = "embryonic stage 4"
    EMBRYONIC_STAGE_5 = "embryonic stage 5"
    EMBRYONIC_STAGE_6 = "embryonic stage 6"
    EMBRYONIC_STAGE_7 = "embryonic stage 7"
    EMBRYONIC_STAGE_8 = "embryonic stage 8"
    EMBRYONIC_STAGE_9 = "embryonic stage 9"
    EXTENDED_GERM_BAND_STAGE = "extended germ band stage"
    FERTILIZED_EGG_STAGE = "fertilized egg stage"
    FIRST_INSTAR_LARVAL_STAGE = "first instar larval stage"
    GASTRULA_STAGE = "gastrula stage"
    IMMATURE_ADULT_STAGE = "immature adult stage"
    LARVAL_STAGE = "larval stage"
    LATE_EMBRYONIC_STAGE = "late embryonic stage"
    LATE_EXTENDED_GERM_BAND_STAGE = "late extended germ band stage"
    LATE_THIRD_INSTAR_LARVAL_STAGE = "late third instar larval stage"
    LIFE_STAGE = "life stage"
    MATURE_ADULT_STAGE = "mature adult stage"
    OOGENESIS = "oogenesis"
    OOGENESIS_STAGE_S1 = "oogenesis stage S1"
    OOGENESIS_STAGE_S10 = "oogenesis stage S10"
    OOGENESIS_STAGE_S10A = "oogenesis stage S10A"
    OOGENESIS_STAGE_S10B = "oogenesis stage S10B"
    OOGENESIS_STAGE_S11 = "oogenesis stage S11"
    OOGENESIS_STAGE_S11A = "oogenesis stage S11a"
    OOGENESIS_STAGE_S11B = "oogenesis stage S11b"
    OOGENESIS_STAGE_S12 = "oogenesis stage S12"
    OOGENESIS_STAGE_S12A = "oogenesis stage S12A"
    OOGENESIS_STAGE_S12B = "oogenesis stage S12B"
    OOGENESIS_STAGE_S12C = "oogenesis stage S12C"
    OOGENESIS_STAGE_S13 = "oogenesis stage S13"
    OOGENESIS_STAGE_S13A = "oogenesis stage S13A"
    OOGENESIS_STAGE_S13B = "oogenesis stage S13B"
    OOGENESIS_STAGE_S13C = "oogenesis stage S13C"
    OOGENESIS_STAGE_S13D = "oogenesis stage S13D"
    OOGENESIS_STAGE_S13E = "oogenesis stage S13E"
    OOGENESIS_STAGE_S14 = "oogenesis stage S14"
    OOGENESIS_STAGE_S14A = "oogenesis stage S14A"
    OOGENESIS_STAGE_S14B = "oogenesis stage S14B"
    OOGENESIS_STAGE_S2 = "oogenesis stage S2"
    OOGENESIS_STAGE_S3 = "oogenesis stage S3"
    OOGENESIS_STAGE_S4 = "oogenesis stage S4"
    OOGENESIS_STAGE_S5 = "oogenesis stage S5"
    OOGENESIS_STAGE_S6 = "oogenesis stage S6"
    OOGENESIS_STAGE_S7 = "oogenesis stage S7"
    OOGENESIS_STAGE_S8 = "oogenesis stage S8"
    OOGENESIS_STAGE_S9 = "oogenesis stage S9"
    PHARATE_ADULT_STAGE = "pharate adult stage"
    PHARATE_ADULT_STAGE_P10 = "pharate adult stage P10"
    PHARATE_ADULT_STAGE_P11 = "pharate adult stage P11"
    PHARATE_ADULT_STAGE_P11_I_ = "pharate adult stage P11(i)"
    PHARATE_ADULT_STAGE_P11_II_ = "pharate adult stage P11(ii)"
    PHARATE_ADULT_STAGE_P12 = "pharate adult stage P12"
    PHARATE_ADULT_STAGE_P12_I_ = "pharate adult stage P12(i)"
    PHARATE_ADULT_STAGE_P12_II_ = "pharate adult stage P12(ii)"
    PHARATE_ADULT_STAGE_P13 = "pharate adult stage P13"
    PHARATE_ADULT_STAGE_P14 = "pharate adult stage P14"
    PHARATE_ADULT_STAGE_P15 = "pharate adult stage P15"
    PHARATE_ADULT_STAGE_P15_I_ = "pharate adult stage P15(i)"
    PHARATE_ADULT_STAGE_P15_II_ = "pharate adult stage P15(ii)"
    PHARATE_ADULT_STAGE_P8 = "pharate adult stage P8"
    PHARATE_ADULT_STAGE_P9 = "pharate adult stage P9"
    PRE_BLASTODERM_STAGE = "pre-blastoderm stage"
    PREPUPAL_STAGE = "prepupal stage"
    PREPUPAL_STAGE_P1 = "prepupal stage P1"
    PREPUPAL_STAGE_P2 = "prepupal stage P2"
    PREPUPAL_STAGE_P3 = "prepupal stage P3"
    PREPUPAL_STAGE_P4 = "prepupal stage P4"
    PREPUPAL_STAGE_P4_I_ = "prepupal stage P4(i)"
    PREPUPAL_STAGE_P4_II_ = "prepupal stage P4(ii)"
    PUPAL_STAGE = "pupal stage"
    PUPAL_STAGE_P5 = "pupal stage P5"
    PUPAL_STAGE_P5_I_ = "pupal stage P5(i)"
    PUPAL_STAGE_P5_II_ = "pupal stage P5(ii)"
    PUPAL_STAGE_P6 = "pupal stage P6"
    PUPAL_STAGE_P7 = "pupal stage P7"
    SECOND_INSTAR_LARVAL_STAGE = "second instar larval stage"
    SPERMATOGENESIS = "spermatogenesis"
    THIRD_INSTAR___CLEARED_GUT_STAGE = "third instar - cleared gut stage"
    THIRD_INSTAR___PARTIALLY_CLEARED_GUT_STAGE = "third instar - partially cleared gut stage"
    THIRD_INSTAR___UNCLEARED_GUT_STAGE = "third instar - uncleared gut stage"
    THIRD_INSTAR_LARVAL_STAGE = "third instar larval stage"
    THIRD_INSTAR_LARVAL_STAGE_L1 = "third instar larval stage L1"
    THIRD_INSTAR_LARVAL_STAGE_L2 = "third instar larval stage L2"
    UNFERTILIZED_EGG_STAGE = "unfertilized egg stage"
    WANDERING_THIRD_INSTAR_LARVAL_STAGE = "wandering third instar larval stage"
