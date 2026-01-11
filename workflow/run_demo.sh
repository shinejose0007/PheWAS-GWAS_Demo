#!/usr/bin/env bash
# Simple workflow script to generate demo data and run a quick association script (non-interactive)
python3 src/generate_data.py
echo "Demo data generated in data/"
echo "To run the Streamlit app locally: streamlit run app.py"
