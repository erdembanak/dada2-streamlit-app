# DADA2 Genetic Referral Score

Standalone Streamlit calculator for the DADA2 Genetic Referral Score.

Scoring rule:
- Bicytopenia `+5`
- Musculoskeletal involvement `+4`
- Hypogammaglobulinemia `+4`
- Neurologic involvement `+3`
- High acute phase reactants `+2`
- Family history `+2`
- Skin involvement `+1`
- Consanguinity `+1`
- Thrombocytosis `-3`
- Threshold `>= 10`

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notes

- This app does not load, display, or store any existing patient data.
