#!/bin/bash
python src/pipelines/sc-update/00-scrape-data.py
python src/pipelines/sc-update/01-feature-engineering.py
python src/pipelines/sc-update/02-update-predictions.py