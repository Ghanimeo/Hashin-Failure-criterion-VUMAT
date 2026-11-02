"""Glass -> flax / flax-glass hybrid substitution engine.

Given a reference (e.g. glass) laminate and its load case, enumerate bio-based
candidates that keep the reference stacking orientations, and check:
  * membrane stiffness   A11, A22, A66  >= ratio * reference
  * bending stiffness    D11, D22       >= ratio * reference
  * first-ply failure    (Tsai-Wu and Hashin) <= 1/SF under the load case,
    evaluated on environmentally knocked-down properties for flax plies.
Ranks passing candidates by areal mass (or CO2, or cost).
"""
from dataclasses import dataclass, field
import numpy as np

from .clt import Laminate, first_ply_failure
from .materials import Ply, DEFAULT_KD


@dataclass
class Requirement:
    N: tuple = (0.0, 0.0, 0.0)        # N/mm
    M: tuple = (0.0, 0.0, 0.0)        # N*mm/mm
    safety_factor: float = 1.5
    stiffness_ratio: float = 1.0       # 1.0 = equal stiffness to reference
    check_membrane: bool = True
    check_bending: bool = True
    max_thickness: float = 30.0        # mm
    # "match_reference": candidate (knocked-down) first-ply-failure index must not
    #   exceed the reference's, i.e. at least the same load capacity as the part replaced.
    # "absolute": FI * safety_factor <= 1 under the given load case.
    strength_mode: str = "match_reference"


@dataclass
class Candidate:
    label: str
    laminate: Laminate
    passes: bool
    checks: dict = field(default_factory=dict)

    def summary(self, ref: Laminate) -> dict:
        return {
            "candidate": self.label,
            "plies": len(self.laminate.plies),
            "thickness_mm": round(self.laminate.thickness, 2),
            "mass_kg_m2": round(self.laminate.areal_mass, 3),
            "mass_change_%": round(100 * (self.laminate.areal_mass / ref.areal_mass - 1), 1),
            "co2_change_%": round(100 * (self.laminate.co2 / ref.co2 - 1), 1),
            "cost_change_%": round(100 * (self.laminate.cost / ref.cost - 1), 1),
            "passes": self.passes,
            **{k: (float(round(v, 3)) if isinstance(v, float) else v) for k, v in self.checks.items()},
        }


def symmetric(angles_half):
    return list(angles_half) + list(reversed(angles_half))


def _stiffness_ratios(lam: Laminate, ref: Laminate) -> dict:
    A, _, D = lam.abd(); Ar, _, Dr = ref.abd()
    return {"A11": A[0, 0] / Ar[0, 0], "A22": A[1, 1] / Ar[1, 1], "A66": A[2, 2] / Ar[2, 2],
            "D11": D[0, 0] / Dr[0, 0], "D22": D[1, 1] / Dr[1, 1]}


def evaluate(label: str, lam: Laminate, lam_kd: Laminate, ref: Laminate, req: Requirement,
             ref_fi: float = None) -> Candidate:
    r = _stiffness_ratios(lam, ref)
    checks = {}
    ok = True
    keys = (["A11", "A22", "A66"] if req.check_membrane else []) + \
           (["D11", "D22"] if req.check_bending else [])
    for k in keys:
        checks[f"{k}_ratio"] = r[k]
        ok &= r[k] >= req.stiffness_ratio - 1e-9
    has_load = np.any(np.asarray(req.N)) or np.any(np.asarray(req.M))
    if has_load:
        f = first_ply_failure(lam_kd, req.N, req.M)
        checks["FI_tsai_wu_x_SF"] = f["tsai_wu"] * req.safety_factor
        checks["FI_hashin_x_SF"] = f["hashin"] * req.safety_factor
        checks["critical_mode"] = f["hashin_mode"]
        fi = max(f["tsai_wu"], f["hashin"])
        if req.strength_mode == "absolute" or ref_fi is None:
            ok &= fi * req.safety_factor <= 1.0
        else:
            checks["capacity_vs_ref"] = ref_fi / fi if fi > 0 else float("inf")
            ok &= fi <= ref_fi * (1 + 1e-9)
    ok &= lam.thickness <= req.max_thickness
    return Candidate(label, lam, bool(ok), checks)


def _groups(ref_half):
    """Orientation groups; +theta/-theta pairs are kept together (balanced)."""
    groups, seen = [], set()
    for a in ref_half:
        key = abs(a) if a not in (0.0, 90.0) else a
        if key in seen:
            continue
        seen.add(key)
        groups.append([key, -key] if a not in (0.0, 90.0) and -a in ref_half else [a])
    return groups


def _interleave(groups, counts):
    """Build a half-stack (outer -> mid-plane) by cycling through groups."""
    remaining = list(counts); out = []
    while any(remaining):
        for i, g in enumerate(groups):
            if remaining[i]:
                out.extend(g); remaining[i] -= 1
    return out


def translate(ref_half, ref_ply: Ply, bio_ply: Ply, req: Requirement,
              kd=DEFAULT_KD, max_per_group: int = 6, hybrid_ply: Ply = None,
              max_skin: int = 2):
    """ref_half: half-stack angles (outer -> mid-plane) of the symmetric reference.

    Candidates keep the reference orientation set but let the number of plies in
    each orientation group vary (1..max_per_group), optionally with 1..max_skin
    reference-material skin plies per side (hybrid). Flax plies are checked
    with knocked-down properties.
    """
    import itertools
    ref_half = [float(a) for a in ref_half]
    ref = Laminate([(ref_ply, a) for a in symmetric(ref_half)])
    kd_of = lambda p: p.knocked_down(kd["stiffness"], kd["strength"]) if p.moisture_sensitive else p
    skin_ply = hybrid_ply or ref_ply
    groups = _groups(ref_half)

    ref_fi = None
    if np.any(np.asarray(req.N)) or np.any(np.asarray(req.M)):
        f = first_ply_failure(ref, req.N, req.M)
        ref_fi = max(f["tsai_wu"], f["hashin"])
    out = [evaluate("reference", ref, ref, ref, req, ref_fi)]
    for counts in itertools.product(range(0, max_per_group + 1), repeat=len(groups)):
        if not any(counts):
            continue
        core = _interleave(groups, counts)
        tag = ",".join(f"{'/'.join(f'{a:g}' for a in g)}:{c}" for g, c in zip(groups, counts))
        for k in range(0, max_skin + 1):
            skins = [ref_half[i % len(ref_half)] for i in range(k)]
            half = [(skin_ply, a) for a in skins] + [(bio_ply, a) for a in core]
            lam = Laminate(half + list(reversed(half)))
            lam_kd = Laminate([(kd_of(p), a) for p, a in lam.plies])
            label = (f"hybrid {k} skin/side + bio[{tag}]" if k else f"bio[{tag}]")
            out.append(evaluate(label, lam, lam_kd, ref, req, ref_fi))
    return ref, out


def symmetric_plies(half_bottom_up):
    """half listed bottom(outer) -> mid-plane; mirror to full laminate."""
    return list(half_bottom_up) + list(reversed(half_bottom_up))


def best(ref, cands, objective="mass_kg_m2", top=5):
    rows = [c.summary(ref) for c in cands if c.label != "reference" and c.passes]
    return sorted(rows, key=lambda r: r[objective if objective in r else "mass_kg_m2"])[:top]
