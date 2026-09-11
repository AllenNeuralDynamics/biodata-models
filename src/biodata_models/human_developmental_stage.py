"""Human developmental stage"""

import requests
from pydantic import BaseModel, ConfigDict

from biodata_models.registries import Registry

"""Human developmental stage"""


class HumanDevelopmentalStageModel(BaseModel):
    """Base model for human developmental stage"""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry
    registry_identifier: str


def search_hsapdv_exact_match(class_name):
    """Pull the exact name match from the HSAPDV ontology

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
        "ontology": "hsapdv",  # Specify the ontology
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


def get_hsapdv_id(class_name):
    """Get the HSAPDV ID for a given class name

    Parameters
    ----------
    class_name : str

    Returns
    -------
    int
    """
    results = search_hsapdv_exact_match(class_name)

    if results:
        return results[0]["iri"].split("_")[1]
    else:
        return None


class HumanDevelopmentalStageMeta(type):
    """Meta class for HumanDevelopmentalStage groups"""

    def __getattribute__(cls, name):
        """Custom get attribute function, validates developmental stage names against external HSAPDV registry

        Parameters
        ----------
        name : str
            Attribute name

        Raises
        ------
        ValueError
            Name not found in the HSAPDV registry
        """

        # bypass
        if name.startswith("__"):
            return object.__getattribute__(cls, name)

        class_dict = object.__getattribute__(cls, "__dict__")

        if name in class_dict:
            original_name = super().__getattribute__(name)

            hsapdv_id = get_hsapdv_id(original_name)

            if hsapdv_id:
                return HumanDevelopmentalStageModel(
                    name=original_name,
                    registry=Registry.HSAPDV,
                    registry_identifier=hsapdv_id,
                )
            else:
                raise ValueError(f"Could not find HSAPDV ID for {original_name}")

        # second bypass for defined values
        return super().__getattribute__(name)


class HumanDevelopmentalStage(metaclass=HumanDevelopmentalStageMeta):
    """Human developmental stage"""

    _1_MONTH_OLD_STAGE = "1-month-old stage"
    _1_YEAR_OLD_STAGE = "1-year-old stage"
    _10_MONTH_OLD_STAGE = "10-month-old stage"
    _10_YEAR_OLD_STAGE = "10-year-old stage"
    _100_YEAR_OLD_STAGE = "100-year-old stage"
    _101_YEAR_OLD_STAGE = "101-year-old stage"
    _102_YEAR_OLD_STAGE = "102-year-old stage"
    _103_YEAR_OLD_STAGE = "103-year-old stage"
    _104_YEAR_OLD_STAGE = "104-year-old stage"
    _105_YEAR_OLD_STAGE = "105-year-old stage"
    _106_YEAR_OLD_STAGE = "106-year-old stage"
    _107_YEAR_OLD_STAGE = "107-year-old stage"
    _108_YEAR_OLD_STAGE = "108-year-old stage"
    _109_YEAR_OLD_STAGE = "109-year-old stage"
    _10TH_WEEK_POST_FERTILIZATION_STAGE = "10th week post-fertilization stage"
    _11_MONTH_OLD_STAGE = "11-month-old stage"
    _11_YEAR_OLD_STAGE = "11-year-old stage"
    _110_YEAR_OLD_STAGE = "110-year-old stage"
    _111_YEAR_OLD_STAGE = "111-year-old stage"
    _112_YEAR_OLD_STAGE = "112-year-old stage"
    _113_YEAR_OLD_STAGE = "113-year-old stage"
    _114_YEAR_OLD_STAGE = "114-year-old stage"
    _11TH_WEEK_POST_FERTILIZATION_STAGE = "11th week post-fertilization stage"
    _12_MONTH_OLD_STAGE = "12-month-old stage"
    _12_YEAR_OLD_STAGE = "12-year-old stage"
    _12TH_WEEK_POST_FERTILIZATION_STAGE = "12th week post-fertilization stage"
    _13_MONTH_OLD_STAGE = "13-month-old stage"
    _13_YEAR_OLD_STAGE = "13-year-old stage"
    _13TH_WEEK_POST_FERTILIZATION_STAGE = "13th week post-fertilization stage"
    _14_MONTH_OLD_STAGE = "14-month-old stage"
    _14_YEAR_OLD_STAGE = "14-year-old stage"
    _14TH_WEEK_POST_FERTILIZATION_STAGE = "14th week post-fertilization stage"
    _15_19_YEAR_OLD = "15-19 year-old"
    _15_MONTH_OLD_STAGE = "15-month-old stage"
    _15_YEAR_OLD_STAGE = "15-year-old stage"
    _15TH_WEEK_POST_FERTILIZATION_STAGE = "15th week post-fertilization stage"
    _16_MONTH_OLD_STAGE = "16-month-old stage"
    _16_YEAR_OLD_STAGE = "16-year-old stage"
    _16TH_WEEK_POST_FERTILIZATION_STAGE = "16th week post-fertilization stage"
    _17_MONTH_OLD_STAGE = "17-month-old stage"
    _17_YEAR_OLD_STAGE = "17-year-old stage"
    _17TH_WEEK_POST_FERTILIZATION_STAGE = "17th week post-fertilization stage"
    _18_MONTH_OLD_STAGE = "18-month-old stage"
    _18_YEAR_OLD_STAGE = "18-year-old stage"
    _18TH_WEEK_POST_FERTILIZATION_STAGE = "18th week post-fertilization stage"
    _19_MONTH_OLD_STAGE = "19-month-old stage"
    _19_YEAR_OLD_STAGE = "19-year-old stage"
    _19TH_WEEK_POST_FERTILIZATION_STAGE = "19th week post-fertilization stage"
    _2_4_YEAR_OLD_CHILD_STAGE = "2-4 year-old child stage"
    _2_MONTH_OLD_STAGE = "2-month-old stage"
    _2_YEAR_OLD_STAGE = "2-year-old stage"
    _20_MONTH_OLD_STAGE = "20-month-old stage"
    _20_YEAR_OLD_STAGE = "20-year-old stage"
    _20TH_WEEK_POST_FERTILIZATION_STAGE = "20th week post-fertilization stage"
    _21_MONTH_OLD_STAGE = "21-month-old stage"
    _21_YEAR_OLD_STAGE = "21-year-old stage"
    _21ST_WEEK_POST_FERTILIZATION_STAGE = "21st week post-fertilization stage"
    _22_MONTH_OLD_STAGE = "22-month-old stage"
    _22_YEAR_OLD_STAGE = "22-year-old stage"
    _22ND_WEEK_POST_FERTILIZATION_STAGE = "22nd week post-fertilization stage"
    _23_MONTH_OLD_STAGE = "23-month-old stage"
    _23_YEAR_OLD_STAGE = "23-year-old stage"
    _23RD_WEEK_POST_FERTILIZATION_STAGE = "23rd week post-fertilization stage"
    _24_YEAR_OLD_STAGE = "24-year-old stage"
    _24TH_WEEK_POST_FERTILIZATION_STAGE = "24th week post-fertilization stage"
    _25_YEAR_OLD_STAGE = "25-year-old stage"
    _25TH_WEEK_POST_FERTILIZATION_STAGE = "25th week post-fertilization stage"
    _26_YEAR_OLD_STAGE = "26-year-old stage"
    _26TH_WEEK_POST_FERTILIZATION_STAGE = "26th week post-fertilization stage"
    _27_YEAR_OLD_STAGE = "27-year-old stage"
    _27TH_WEEK_POST_FERTILIZATION_STAGE = "27th week post-fertilization stage"
    _28_YEAR_OLD_STAGE = "28-year-old stage"
    _28TH_WEEK_POST_FERTILIZATION_STAGE = "28th week post-fertilization stage"
    _29_YEAR_OLD_STAGE = "29-year-old stage"
    _29TH_WEEK_POST_FERTILIZATION_STAGE = "29th week post-fertilization stage"
    _3_MONTH_OLD_STAGE = "3-month-old stage"
    _3_YEAR_OLD_STAGE = "3-year-old stage"
    _30_YEAR_OLD_STAGE = "30-year-old stage"
    _30TH_WEEK_POST_FERTILIZATION_STAGE = "30th week post-fertilization stage"
    _31_YEAR_OLD_STAGE = "31-year-old stage"
    _31ST_WEEK_POST_FERTILIZATION_STAGE = "31st week post-fertilization stage"
    _32_YEAR_OLD_STAGE = "32-year-old stage"
    _32ND_WEEK_POST_FERTILIZATION_STAGE = "32nd week post-fertilization stage"
    _33_YEAR_OLD_STAGE = "33-year-old stage"
    _33RD_WEEK_POST_FERTILIZATION_STAGE = "33rd week post-fertilization stage"
    _34_YEAR_OLD_STAGE = "34-year-old stage"
    _34TH_WEEK_POST_FERTILIZATION_STAGE = "34th week post-fertilization stage"
    _35_YEAR_OLD_STAGE = "35-year-old stage"
    _35TH_WEEK_POST_FERTILIZATION_STAGE = "35th week post-fertilization stage"
    _36_YEAR_OLD_STAGE = "36-year-old stage"
    _36TH_WEEK_POST_FERTILIZATION_STAGE = "36th week post-fertilization stage"
    _37_YEAR_OLD_STAGE = "37-year-old stage"
    _37TH_WEEK_POST_FERTILIZATION_STAGE = "37th week post-fertilization stage"
    _38_YEAR_OLD_STAGE = "38-year-old stage"
    _38TH_WEEK_POST_FERTILIZATION_AND_OVER_STAGE = "38th week post-fertilization and over stage"
    _39_YEAR_OLD_STAGE = "39-year-old stage"
    _4_MONTH_OLD_STAGE = "4-month-old stage"
    _4_YEAR_OLD_STAGE = "4-year-old stage"
    _40_YEAR_OLD_STAGE = "40-year-old stage"
    _41_YEAR_OLD_STAGE = "41-year-old stage"
    _42_YEAR_OLD_STAGE = "42-year-old stage"
    _43_YEAR_OLD_STAGE = "43-year-old stage"
    _44_YEAR_OLD_STAGE = "44-year-old stage"
    _45_YEAR_OLD_STAGE = "45-year-old stage"
    _46_YEAR_OLD_STAGE = "46-year-old stage"
    _47_YEAR_OLD_STAGE = "47-year-old stage"
    _48_YEAR_OLD_STAGE = "48-year-old stage"
    _49_YEAR_OLD_STAGE = "49-year-old stage"
    _5_MONTH_OLD_STAGE = "5-month-old stage"
    _5_YEAR_OLD_STAGE = "5-year-old stage"
    _50_YEAR_OLD_STAGE = "50-year-old stage"
    _51_YEAR_OLD_STAGE = "51-year-old stage"
    _52_YEAR_OLD_STAGE = "52-year-old stage"
    _53_YEAR_OLD_STAGE = "53-year-old stage"
    _54_YEAR_OLD_STAGE = "54-year-old stage"
    _55_YEAR_OLD_STAGE = "55-year-old stage"
    _56_YEAR_OLD_STAGE = "56-year-old stage"
    _57_YEAR_OLD_STAGE = "57-year-old stage"
    _58_YEAR_OLD_STAGE = "58-year-old stage"
    _59_YEAR_OLD_STAGE = "59-year-old stage"
    _6_MONTH_OLD_STAGE = "6-month-old stage"
    _6_YEAR_OLD_STAGE = "6-year-old stage"
    _60_79_YEAR_OLD_STAGE = "60-79 year-old stage"
    _60_YEAR_OLD_STAGE = "60-year-old stage"
    _61_YEAR_OLD_STAGE = "61-year-old stage"
    _62_YEAR_OLD_STAGE = "62-year-old stage"
    _63_YEAR_OLD_STAGE = "63-year-old stage"
    _64_YEAR_OLD_STAGE = "64-year-old stage"
    _65_YEAR_OLD_STAGE = "65-year-old stage"
    _66_YEAR_OLD_STAGE = "66-year-old stage"
    _67_YEAR_OLD_STAGE = "67-year-old stage"
    _68_YEAR_OLD_STAGE = "68-year-old stage"
    _69_YEAR_OLD_STAGE = "69-year-old stage"
    _7_MONTH_OLD_STAGE = "7-month-old stage"
    _7_YEAR_OLD_STAGE = "7-year-old stage"
    _70_YEAR_OLD_STAGE = "70-year-old stage"
    _71_YEAR_OLD_STAGE = "71-year-old stage"
    _72_YEAR_OLD_STAGE = "72-year-old stage"
    _73_YEAR_OLD_STAGE = "73-year-old stage"
    _74_YEAR_OLD_STAGE = "74-year-old stage"
    _75_YEAR_OLD_STAGE = "75-year-old stage"
    _76_YEAR_OLD_STAGE = "76-year-old stage"
    _77_YEAR_OLD_STAGE = "77-year-old stage"
    _78_YEAR_OLD_STAGE = "78-year-old stage"
    _79_YEAR_OLD_STAGE = "79-year-old stage"
    _8_MONTH_OLD_STAGE = "8-month-old stage"
    _8_YEAR_OLD_STAGE = "8-year-old stage"
    _80_YEAR_OLD_AND_OVER_STAGE = "80 year-old and over stage"
    _80_YEAR_OLD_STAGE = "80-year-old stage"
    _81_YEAR_OLD_STAGE = "81-year-old stage"
    _82_YEAR_OLD_STAGE = "82-year-old stage"
    _83_YEAR_OLD_STAGE = "83-year-old stage"
    _84_YEAR_OLD_STAGE = "84-year-old stage"
    _85_YEAR_OLD_STAGE = "85-year-old stage"
    _86_YEAR_OLD_STAGE = "86-year-old stage"
    _87_YEAR_OLD_STAGE = "87-year-old stage"
    _88_YEAR_OLD_STAGE = "88-year-old stage"
    _89_YEAR_OLD_STAGE = "89-year-old stage"
    _9_MONTH_OLD_STAGE = "9-month-old stage"
    _9_YEAR_OLD_STAGE = "9-year-old stage"
    _90_YEAR_OLD_AND_OVER_STAGE = "90 year-old and over stage"
    _90_YEAR_OLD_STAGE = "90-year-old stage"
    _91_YEAR_OLD_STAGE = "91-year-old stage"
    _92_YEAR_OLD_STAGE = "92-year-old stage"
    _93_YEAR_OLD_STAGE = "93-year-old stage"
    _94_YEAR_OLD_STAGE = "94-year-old stage"
    _95_YEAR_OLD_STAGE = "95-year-old stage"
    _96_YEAR_OLD_STAGE = "96-year-old stage"
    _97_YEAR_OLD_STAGE = "97-year-old stage"
    _98_YEAR_OLD_STAGE = "98-year-old stage"
    _99_YEAR_OLD_STAGE = "99-year-old stage"
    _9TH_WEEK_POST_FERTILIZATION_STAGE = "9th week post-fertilization stage"
    CARNEGIE_STAGE_01 = "Carnegie stage 01"
    CARNEGIE_STAGE_02 = "Carnegie stage 02"
    CARNEGIE_STAGE_03 = "Carnegie stage 03"
    CARNEGIE_STAGE_04 = "Carnegie stage 04"
    CARNEGIE_STAGE_05 = "Carnegie stage 05"
    CARNEGIE_STAGE_05A = "Carnegie stage 05a"
    CARNEGIE_STAGE_05B = "Carnegie stage 05b"
    CARNEGIE_STAGE_05C = "Carnegie stage 05c"
    CARNEGIE_STAGE_06 = "Carnegie stage 06"
    CARNEGIE_STAGE_06A = "Carnegie stage 06a"
    CARNEGIE_STAGE_06B = "Carnegie stage 06b"
    CARNEGIE_STAGE_07 = "Carnegie stage 07"
    CARNEGIE_STAGE_08 = "Carnegie stage 08"
    CARNEGIE_STAGE_09 = "Carnegie stage 09"
    CARNEGIE_STAGE_10 = "Carnegie stage 10"
    CARNEGIE_STAGE_11 = "Carnegie stage 11"
    CARNEGIE_STAGE_12 = "Carnegie stage 12"
    CARNEGIE_STAGE_13 = "Carnegie stage 13"
    CARNEGIE_STAGE_14 = "Carnegie stage 14"
    CARNEGIE_STAGE_15 = "Carnegie stage 15"
    CARNEGIE_STAGE_16 = "Carnegie stage 16"
    CARNEGIE_STAGE_17 = "Carnegie stage 17"
    CARNEGIE_STAGE_18 = "Carnegie stage 18"
    CARNEGIE_STAGE_19 = "Carnegie stage 19"
    CARNEGIE_STAGE_20 = "Carnegie stage 20"
    CARNEGIE_STAGE_21 = "Carnegie stage 21"
    CARNEGIE_STAGE_22 = "Carnegie stage 22"
    CARNEGIE_STAGE_23 = "Carnegie stage 23"
    ADULT_STAGE = "adult stage"
    BLASTULA_STAGE = "blastula stage"
    CENTENARIAN_STAGE = "centenarian stage"
    CHILD_STAGE__1_4_YO_ = "child stage (1-4 yo)"
    EIGHTH_LMP_MONTH_STAGE = "eighth LMP month stage"
    EIGHTH_DECADE_STAGE = "eighth decade stage"
    ELEVENTH_DECADE_STAGE = "eleventh decade stage"
    EMBRYONIC_STAGE = "embryonic stage"
    FETAL_STAGE = "fetal stage"
    FIFTH_LMP_MONTH_STAGE = "fifth LMP month stage"
    FIFTH_DECADE_STAGE = "fifth decade stage"
    FOURTH_LMP_MONTH_STAGE = "fourth LMP month stage"
    FOURTH_DECADE_STAGE = "fourth decade stage"
    GASTRULA_STAGE = "gastrula stage"
    INFANT_STAGE = "infant stage"
    JUVENILE_STAGE__5_14_YO_ = "juvenile stage (5-14 yo)"
    LATE_ADULT_STAGE = "late adult stage"
    LIFE_CYCLE = "life cycle"
    LIFE_CYCLE_STAGE = "life cycle stage"
    MIDDLE_AGED_STAGE = "middle aged stage"
    MORULA_STAGE = "morula stage"
    NEURULA_STAGE = "neurula stage"
    NEWBORN_STAGE__0_28_DAYS_ = "newborn stage (0-28 days)"
    NINTH_LMP_MONTH_STAGE = "ninth LMP month stage"
    NINTH_DECADE_STAGE = "ninth decade stage"
    NURSING_STAGE__0_11_MONTHS_ = "nursing stage (0-11 months)"
    ORGANOGENESIS_STAGE = "organogenesis stage"
    PEDIATRIC_STAGE = "pediatric stage"
    POSTNATAL_STAGE = "postnatal stage"
    PRENATAL_STAGE = "prenatal stage"
    PRIME_ADULT_STAGE = "prime adult stage"
    SEVENTH_LMP_MONTH_STAGE = "seventh LMP month stage"
    SEVENTH_DECADE_STAGE = "seventh decade stage"
    SIXTH_LMP_MONTH_STAGE = "sixth LMP month stage"
    SIXTH_DECADE_STAGE = "sixth decade stage"
    TENTH_DECADE_STAGE = "tenth decade stage"
    THIRD_LMP_MONTH_STAGE = "third LMP month stage"
    THIRD_DECADE_STAGE = "third decade stage"
    YOUNG_ADULT_STAGE = "young adult stage"
