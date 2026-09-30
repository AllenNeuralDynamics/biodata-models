# Completing a New Element

1. Find the closest existing model and decide whether the element is generated or hand-maintained. For generated models, update `_generators/models/*.csv` and `_generators/templates/*.txt`; for API-backed or custom models, implement under `src/biodata_models/`.
2. Add any required `Registry` value and update relevant external-registry documentation in `aind-data-schema`.
3. Add `unittest` coverage for normal use, boundary and error cases, and mocked external requests. Document every module, class, function, and test method so Interrogate remains at 100%.
4. For generated models, activate `.venv` and run `./run_all.sh`. Format changes with `black` and `isort`.
5. Validate with `flake8 . && interrogate --verbose .`, then `coverage run -m unittest discover && coverage report`; resolve failures and retain the configured 100% coverage thresholds.