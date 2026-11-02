# Bio-Composite Spec Translator (MVP v0.1)

Turns an existing glass-fibre laminate specification into **flax and flax/glass hybrid** alternatives that keep at least the same stiffness and load capacity. It ranks the alternatives by mass, CO₂, cost or thickness.

> **Screening tool only.** The built-in material values are indicative literature-typical numbers, and the CO₂ and cost factors are placeholders. Replace them with supplier, test and LCA data before you use any result.

## What it checks
- **Classical laminate theory** gives the ABD matrices of the reference and of every candidate.
- **Stiffness:** the membrane terms (A11, A22, A66) and bending terms (D11, D22) must be at least the stiffness ratio times the reference values.
- **Strength:** first-ply failure is checked with **Tsai–Wu and 2D Hashin**. Flax plies are evaluated with environmental knock-downs, which default to 0.75 on strength and 0.90 on stiffness (placeholders). There are two strength modes:
  - `match_reference` (default): the candidate must carry at least the load the reference laminate can carry.
  - `absolute`: the failure index multiplied by the safety factor must not exceed 1 under the given load.
- **Design space:** candidates keep the reference orientation set and vary the ply count in each orientation group, with ±θ pairs kept balanced. Each can optionally have 0–2 reference-material skin plies per side, which makes it a hybrid.

## Run
```bash
pip install -r requirements.txt
python -m biospec.cli --layup 0,45,-45,90 --Nx 100 --Mx 20 --objective co2_change_%
streamlit run app.py
python -m pytest -q tests
```

## Known limitations (roadmap)
- First-ply failure only. Progressive damage is not modelled; the VUMAT in the parent repository could be used for that.
- Flax tensile response is bilinear, but the tool uses the initial modulus only.
- Moisture is a single knock-down factor rather than a function of moisture content.
- There are no buckling, impact, creep or fatigue checks yet.
- The material library is not validated.
