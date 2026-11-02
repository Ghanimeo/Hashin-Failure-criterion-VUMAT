"""Command line: python -m biospec.cli --layup 0,45,-45,90 --Nx 300 --Mx 0"""
import argparse
from .materials import LIBRARY, DEFAULT_KD
from .translator import Requirement, translate, best


def main(argv=None):
    ap = argparse.ArgumentParser(description="Glass -> bio-composite laminate translator (screening only)")
    ap.add_argument("--layup", default="0,45,-45,90", help="half-stack angles of symmetric reference")
    ap.add_argument("--ref", default="glass_ud_epoxy", choices=LIBRARY)
    ap.add_argument("--bio", default="flax_ud_epoxy", choices=LIBRARY)
    for k in ("Nx", "Ny", "Nxy", "Mx", "My", "Mxy"):
        ap.add_argument(f"--{k}", type=float, default=0.0)
    ap.add_argument("--sf", type=float, default=1.5)
    ap.add_argument("--strength-mode", default="match_reference", choices=["match_reference", "absolute"])
    ap.add_argument("--stiffness-ratio", type=float, default=1.0)
    ap.add_argument("--no-membrane", action="store_true")
    ap.add_argument("--no-bending", action="store_true")
    ap.add_argument("--objective", default="mass_kg_m2",
                    choices=["mass_kg_m2", "co2_change_%", "cost_change_%", "thickness_mm"])
    ap.add_argument("--kd-strength", type=float, default=DEFAULT_KD["strength"])
    ap.add_argument("--kd-stiffness", type=float, default=DEFAULT_KD["stiffness"])
    a = ap.parse_args(argv)

    req = Requirement(N=(a.Nx, a.Ny, a.Nxy), M=(a.Mx, a.My, a.Mxy), safety_factor=a.sf,
                      stiffness_ratio=a.stiffness_ratio, check_membrane=not a.no_membrane,
                      check_bending=not a.no_bending, strength_mode=a.strength_mode)
    ref, cands = translate([float(x) for x in a.layup.split(",")], LIBRARY[a.ref], LIBRARY[a.bio], req,
                           kd={"strength": a.kd_strength, "stiffness": a.kd_stiffness})
    print("Reference:", cands[0].summary(ref))
    rows = best(ref, cands, a.objective)
    print(f"\nTop passing candidates by {a.objective}:" if rows else "\nNo candidate passes.")
    for r in rows:
        print(r)
    print("\nSCREENING ONLY: indicative material data; validate with tests before design use.")
    return rows


if __name__ == "__main__":
    main()
