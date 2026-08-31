"""Script to pull developmental stage ontology term names from the EBI OLS4 API.

One-off/manual refresh script (like get_protocols.py) — not run automatically by
run_all.sh. Re-run this and commit the resulting CSVs when an ontology release adds
or renames terms.
"""

import pandas as pd
import requests

API_BASE = "https://www.ebi.ac.uk/ols4/api"

ONTOLOGIES = {
    "mmusdv": "src/biodata_models/_generators/models/mouse_developmental_stage.csv",
    "hsapdv": "src/biodata_models/_generators/models/human_developmental_stage.csv",
    "fbdv": "src/biodata_models/_generators/models/drosophila_developmental_stage.csv",
    "wbls": "src/biodata_models/_generators/models/celegans_developmental_stage.csv",
}


def get_ontology_term_names(ontology: str) -> list[str]:
    """Fetch all current (non-obsolete, natively-defined) term labels for an OLS4 ontology.

    Parameters
    ----------
    ontology : str
        OLS4 ontology id, e.g. "mmusdv"

    Returns
    -------
    list[str]
        Sorted, de-duplicated term labels
    """
    names = set()
    page = 0
    while True:
        response = requests.get(
            f"{API_BASE}/ontologies/{ontology}/terms",
            params={"size": 500, "page": page},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        terms = data.get("_embedded", {}).get("terms", [])
        for term in terms:
            if term.get("is_obsolete") or not term.get("is_defining_ontology"):
                continue
            label = term.get("label")
            if label:
                names.add(label)

        total_pages = data.get("page", {}).get("totalPages", 1)
        page += 1
        if page >= total_pages:
            break

    return sorted(names)


def main():
    """Fetch and save term names for each developmental stage ontology"""
    for ontology, output_csv in ONTOLOGIES.items():
        names = get_ontology_term_names(ontology)
        df = pd.DataFrame({"name": names})
        df.to_csv(output_csv, index=False)
        print(f"{ontology}: wrote {len(names)} terms to {output_csv}")


if __name__ == "__main__":
    main()
