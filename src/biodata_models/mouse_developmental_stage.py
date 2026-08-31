"""Mouse developmental stage"""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

"""Mouse developmental stage"""


class MouseDevelopmentalStageModel(BaseModel):
    """Base model for mouse developmental stage"""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry
    registry_identifier: str


def search_mmusdv_exact_match(class_name):
    """Pull the exact name match from the MMUSDV ontology

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
        "ontology": "mmusdv",  # Specify the ontology
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


def get_mmusdv_id(class_name):
    """Get the MMUSDV ID for a given class name

    Parameters
    ----------
    class_name : str

    Returns
    -------
    int
    """
    results = search_mmusdv_exact_match(class_name)

    if results:
        return results[0]["iri"].split("_")[1]
    else:
        return None


class MouseDevelopmentalStageMeta(type):
    """Meta class for MouseDevelopmentalStage groups"""

    def __getattribute__(cls, name):
        """Custom get attribute function, validates developmental stage names against external MMUSDV registry

        Parameters
        ----------
        name : str
            Attribute name

        Raises
        ------
        ValueError
            Name not found in the MMUSDV registry
        """

        # bypass
        if name.startswith("__"):
            return object.__getattribute__(cls, name)

        class_dict = object.__getattribute__(cls, "__dict__")

        if name in class_dict:
            original_name = super().__getattribute__(name)

            mmusdv_id = get_mmusdv_id(original_name)

            if mmusdv_id:
                return MouseDevelopmentalStageModel(
                    name=original_name,
                    registry=Registry.MMUSDV,
                    registry_identifier=mmusdv_id,
                )
            else:
                raise ValueError(f"Could not find MMUSDV ID for {original_name}")

        # second bypass for defined values
        return super().__getattribute__(name)


class MouseDevelopmentalStage(metaclass=MouseDevelopmentalStageMeta):
    """Mouse developmental stage"""

    _1_WEEK_OLD_STAGE = "1-week-old stage"
    _10_DAY_OLD_STAGE = "10-day-old stage"
    _10_MONTH_OLD_STAGE = "10-month-old stage"
    _10_WEEK_OLD_STAGE = "10-week-old stage"
    _11_DAY_OLD_STAGE = "11-day-old stage"
    _11_MONTH_OLD_STAGE = "11-month-old stage"
    _11_WEEK_OLD_STAGE = "11-week-old stage"
    _12_DAY_OLD_STAGE = "12-day-old stage"
    _12_MONTH_OLD_STAGE = "12-month-old stage"
    _12_WEEK_OLD_STAGE = "12-week-old stage"
    _13_DAY_OLD_STAGE = "13-day-old stage"
    _13_MONTH_OLD_STAGE = "13-month-old stage"
    _13_WEEK_OLD_STAGE = "13-week-old stage"
    _14_MONTH_OLD_STAGE = "14-month-old stage"
    _14_WEEK_OLD_STAGE = "14-week-old stage"
    _15_MONTH_OLD_STAGE = "15-month-old stage"
    _15_WEEK_OLD_STAGE = "15-week-old stage"
    _16_MONTH_OLD_STAGE = "16-month-old stage"
    _16_WEEK_OLD_STAGE = "16-week-old stage"
    _17_MONTH_OLD_STAGE = "17-month-old stage"
    _17_WEEK_OLD_STAGE = "17-week-old stage"
    _18_MONTH_OLD_STAGE = "18-month-old stage"
    _18_WEEK_OLD_STAGE = "18-week-old stage"
    _19_MONTH_OLD_STAGE = "19-month-old stage"
    _19_WEEK_OLD_STAGE = "19-week-old stage"
    _2_MONTH_OLD_STAGE = "2-month-old stage"
    _2_WEEK_OLD_STAGE = "2-week-old stage"
    _20_MONTH_OLD_STAGE = "20-month-old stage"
    _20_MONTH_OLD_STAGE_AND_OVER = "20-month-old stage and over"
    _20_WEEK_OLD_STAGE = "20-week-old stage"
    _21_DAY_OLD_STAGE = "21-day-old stage"
    _21_MONTH_OLD_STAGE = "21-month-old stage"
    _21_WEEK_OLD_STAGE = "21-week-old stage"
    _22_DAY_OLD_STAGE = "22-day-old stage"
    _22_MONTH_OLD_STAGE = "22-month-old stage"
    _22_WEEK_OLD_STAGE = "22-week-old stage"
    _23_DAY_OLD_STAGE = "23-day-old stage"
    _23_MONTH_OLD_STAGE = "23-month-old stage"
    _23_WEEK_OLD_STAGE = "23-week-old stage"
    _24_DAY_OLD_STAGE = "24-day-old stage"
    _24_MONTH_OLD_STAGE = "24-month-old stage"
    _24_WEEK_OLD_STAGE = "24-week-old stage"
    _25_DAY_OLD_STAGE = "25-day-old stage"
    _25_MONTH_OLD_STAGE = "25-month-old stage"
    _25_WEEK_OLD_STAGE = "25-week-old stage"
    _26_DAY_OLD_STAGE = "26-day-old stage"
    _26_MONTH_OLD_STAGE = "26-month-old stage"
    _26_WEEK_OLD_STAGE = "26-week-old stage"
    _27_DAY_OLD_STAGE = "27-day-old stage"
    _27_MONTH_OLD_STAGE = "27-month-old stage"
    _27_WEEK_OLD_STAGE = "27-week-old stage"
    _28_MONTH_OLD_STAGE = "28-month-old stage"
    _28_WEEK_OLD_STAGE = "28-week-old stage"
    _29_MONTH_OLD_STAGE = "29-month-old stage"
    _29_WEEK_OLD_STAGE = "29-week-old stage"
    _3_6_MONTH_OLD_MATURE_STAGE = "3-6 month-old mature stage"
    _3_MONTH_OLD_STAGE = "3-month-old stage"
    _30_MONTH_OLD_STAGE = "30-month-old stage"
    _4_6_DAYS = "4-6 days"
    _4_DAY_OLD_STAGE = "4-day-old stage"
    _4_MONTH_OLD_STAGE = "4-month-old stage"
    _4_WEEK_OLD_STAGE = "4-week-old stage"
    _5_DAY_OLD_STAGE = "5-day-old stage"
    _5_MONTH_OLD_STAGE = "5-month-old stage"
    _5_WEEK_OLD_STAGE = "5-week-old stage"
    _6_DAY_OLD_STAGE = "6-day-old stage"
    _6_MONTH_OLD_STAGE = "6-month-old stage"
    _6_WEEK_OLD_STAGE = "6-week-old stage"
    _7_DAY_OLD_STAGE = "7-day-old stage"
    _7_MONTH_OLD_STAGE = "7-month-old stage"
    _7_WEEK_OLD_STAGE = "7-week-old stage"
    _8_DAY_OLD_STAGE = "8-day-old stage"
    _8_MONTH_OLD_STAGE = "8-month-old stage"
    _8_WEEK_OLD_STAGE = "8-week-old stage"
    _9_DAY_OLD_STAGE = "9-day-old stage"
    _9_MONTH_OLD_STAGE = "9-month-old stage"
    _9_WEEK_OLD_STAGE = "9-week-old stage"
    THEILER_STAGE_01 = "Theiler stage 01"
    THEILER_STAGE_02 = "Theiler stage 02"
    THEILER_STAGE_03 = "Theiler stage 03"
    THEILER_STAGE_04 = "Theiler stage 04"
    THEILER_STAGE_05 = "Theiler stage 05"
    THEILER_STAGE_06 = "Theiler stage 06"
    THEILER_STAGE_07 = "Theiler stage 07"
    THEILER_STAGE_08 = "Theiler stage 08"
    THEILER_STAGE_09 = "Theiler stage 09"
    THEILER_STAGE_09A = "Theiler stage 09a"
    THEILER_STAGE_09B = "Theiler stage 09b"
    THEILER_STAGE_10 = "Theiler stage 10"
    THEILER_STAGE_10A = "Theiler stage 10a"
    THEILER_STAGE_10B = "Theiler stage 10b"
    THEILER_STAGE_10C = "Theiler stage 10c"
    THEILER_STAGE_11 = "Theiler stage 11"
    THEILER_STAGE_11A = "Theiler stage 11a"
    THEILER_STAGE_11B = "Theiler stage 11b"
    THEILER_STAGE_11C = "Theiler stage 11c"
    THEILER_STAGE_11D = "Theiler stage 11d"
    THEILER_STAGE_12 = "Theiler stage 12"
    THEILER_STAGE_12A = "Theiler stage 12a"
    THEILER_STAGE_12B = "Theiler stage 12b"
    THEILER_STAGE_13 = "Theiler stage 13"
    THEILER_STAGE_14 = "Theiler stage 14"
    THEILER_STAGE_15 = "Theiler stage 15"
    THEILER_STAGE_16 = "Theiler stage 16"
    THEILER_STAGE_17 = "Theiler stage 17"
    THEILER_STAGE_18 = "Theiler stage 18"
    THEILER_STAGE_19 = "Theiler stage 19"
    THEILER_STAGE_20 = "Theiler stage 20"
    THEILER_STAGE_21 = "Theiler stage 21"
    THEILER_STAGE_22 = "Theiler stage 22"
    THEILER_STAGE_23 = "Theiler stage 23"
    THEILER_STAGE_24 = "Theiler stage 24"
    THEILER_STAGE_25 = "Theiler stage 25"
    THEILER_STAGE_26 = "Theiler stage 26"
    THEILER_STAGE_27 = "Theiler stage 27"
    BLASTULA_STAGE = "blastula stage"
    CLEAVAGE_STAGE = "cleavage stage"
    EMBRYONIC_STAGE = "embryonic stage"
    FETAL_STAGE = "fetal stage"
    GASTRULA_STAGE = "gastrula stage"
    IMMATURE_STAGE = "immature stage"
    INFANT_STAGE = "infant stage"
    JUVENILE_STAGE = "juvenile stage"
    LATE_ADULT_STAGE = "late adult stage"
    LIFE_CYCLE = "life cycle"
    LIFE_CYCLE_STAGE = "life cycle stage"
    MATURE_STAGE = "mature stage"
    MIDDLE_AGED_STAGE = "middle aged stage"
    NURSING_STAGE = "nursing stage"
    ORGANOGENESIS_STAGE = "organogenesis stage"
    POSTNATAL_STAGE = "postnatal stage"
    PRENATAL_STAGE = "prenatal stage"
    PRIME_ADULT_STAGE = "prime adult stage"
    YOUNG_ADULT_STAGE = "young adult stage"
