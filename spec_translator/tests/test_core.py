import numpy as np
from biospec import LIBRARY, Laminate, Requirement, translate, best
from biospec.clt import qbar, first_ply_failure

G, F = LIBRARY["glass_ud_epoxy"], LIBRARY["flax_ud_epoxy"]


def test_qbar_rotation_90_swaps_axes():
    Q0, Q90 = qbar(G, 0), qbar(G, 90)
    assert np.isclose(Q0[0, 0], Q90[1, 1]) and np.isclose(Q0[2, 2], Q90[2, 2])


def test_symmetric_laminate_has_zero_B():
    lam = Laminate([(G, a) for a in [0, 45, -45, 90, 90, -45, 45, 0]])
    _, B, _ = lam.abd()
    assert np.allclose(B, 0, atol=1e-6)


def test_uniaxial_ud_failure_at_Xt():
    lam = Laminate([(G, 0)] * 4)
    h = lam.thickness
    f = first_ply_failure(lam, (G.Xt * h, 0, 0), (0, 0, 0))
    assert np.isclose(f["hashin"], 1.0, rtol=1e-3)
    assert "fibre tension" in f["hashin_mode"]


def test_reference_passes_itself_and_flax_needs_more_thickness():
    req = Requirement(N=(100, 0, 0), stiffness_ratio=1.0)
    ref, cands = translate([0, 45, -45, 90], G, F, req, max_per_group=3)
    assert cands[0].passes
    rows = best(ref, cands)
    assert rows, "expected at least one passing bio/hybrid candidate"
    assert all(r["thickness_mm"] > ref.thickness for r in rows if "hybrid" not in r["candidate"])
    assert all(r["A11_ratio"] >= 1 and r["D11_ratio"] >= 1 for r in rows)


def test_balanced_groups_keep_pm45_paired():
    from biospec.translator import _groups, _interleave
    g = _groups([0, 45, -45, 90])
    assert [45.0, -45.0] in g
    half = _interleave(g, [1, 2, 1])
    assert half.count(45.0) == half.count(-45.0) == 2
