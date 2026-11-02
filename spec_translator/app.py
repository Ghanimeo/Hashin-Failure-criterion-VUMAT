"""Streamlit UI: streamlit run app.py"""
import pandas as pd
import streamlit as st
from dataclasses import replace

from biospec import LIBRARY, DEFAULT_KD, Requirement, translate, best

st.set_page_config(page_title="Bio-Composite Spec Translator", layout="wide")
st.title("Bio-Composite Spec Translator")
st.caption("Glass to flax / flax-hybrid laminate substitution. SCREENING ONLY: indicative data, "
           "validate with coupon and component tests before design use.")

with st.sidebar:
    st.header("Reference part")
    layup = st.text_input("Half-stack angles (outer to mid-plane)", "0,45,-45,90")
    ref_key = st.selectbox("Reference ply", list(LIBRARY), index=0)
    bio_key = st.selectbox("Bio ply", list(LIBRARY), index=1)
    st.header("Load case (per unit width)")
    c1, c2 = st.columns(2)
    Nx = c1.number_input("Nx [N/mm]", value=100.0); Mx = c2.number_input("Mx [N]", value=20.0)
    Ny = c1.number_input("Ny [N/mm]", value=0.0); My = c2.number_input("My [N]", value=0.0)
    Nxy = c1.number_input("Nxy [N/mm]", value=0.0); Mxy = c2.number_input("Mxy [N]", value=0.0)
    st.header("Requirements")
    mode = st.radio("Strength check", ["match_reference", "absolute"])
    sf = st.number_input("Safety factor (absolute mode)", value=1.5)
    sr = st.number_input("Stiffness ratio vs reference", value=1.0, step=0.05)
    memb = st.checkbox("Membrane stiffness (A)", True); bend = st.checkbox("Bending stiffness (D)", True)
    st.header("Environmental knock-down (flax)")
    kd_s = st.slider("Strength KD", 0.4, 1.0, DEFAULT_KD["strength"])
    kd_e = st.slider("Stiffness KD", 0.5, 1.0, DEFAULT_KD["stiffness"])
    objective = st.selectbox("Rank by", ["mass_kg_m2", "co2_change_%", "cost_change_%", "thickness_mm"])
    maxg = st.slider("Max plies per orientation group", 1, 8, 5)

st.subheader("Material data (edit to your supplier / test values)")
mat_df = pd.DataFrame({k: vars(LIBRARY[k]) for k in {ref_key, bio_key}}).drop(["name", "notes"])
mat_df = st.data_editor(mat_df)


def ply_from(key):
    vals = {f: type(getattr(LIBRARY[key], f))(mat_df.loc[f, key]) for f in mat_df.index}
    return replace(LIBRARY[key], **vals)


if st.button("Translate", type="primary"):
    req = Requirement(N=(Nx, Ny, Nxy), M=(Mx, My, Mxy), safety_factor=sf, stiffness_ratio=sr,
                      check_membrane=memb, check_bending=bend, strength_mode=mode)
    ref, cands = translate([float(a) for a in layup.split(",")], ply_from(ref_key), ply_from(bio_key),
                           req, kd={"strength": kd_s, "stiffness": kd_e}, max_per_group=maxg)
    st.write("**Reference**", pd.DataFrame([cands[0].summary(ref)]))
    rows = best(ref, cands, objective, top=10)
    if rows:
        df = pd.DataFrame(rows)
        st.write(f"**Top passing candidates** ({sum(c.passes for c in cands[1:])} of {len(cands) - 1} pass)")
        st.dataframe(df)
        st.download_button("Download spec sheet (CSV)", df.to_csv(index=False), "bio_spec_candidates.csv")
        allc = pd.DataFrame([c.summary(ref) for c in cands[1:]])
        st.scatter_chart(allc, x="mass_change_%", y="co2_change_%", color="passes")
    else:
        st.error("No candidate meets all requirements. Relax stiffness ratio, raise max plies, or allow hybrids.")
