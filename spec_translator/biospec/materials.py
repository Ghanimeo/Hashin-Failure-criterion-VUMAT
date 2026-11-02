"""Ply material library.

All default values are INDICATIVE, typical of the open literature, and intended
for screening only. Replace with supplier or in-house test data before any
design use. CO2 factors are placeholders: supply your own LCA values.
"""
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Ply:
    name: str
    E1: float      # MPa
    E2: float      # MPa
    G12: float     # MPa
    nu12: float
    Xt: float      # MPa
    Xc: float      # MPa
    Yt: float      # MPa
    Yc: float      # MPa
    S: float       # MPa
    t: float       # mm, cured ply thickness
    rho: float     # g/cm3
    co2: float     # kg CO2-eq per kg laminate (placeholder)
    cost: float    # EUR per kg laminate (placeholder)
    moisture_sensitive: bool = False
    notes: str = ""

    def knocked_down(self, stiffness_kd: float, strength_kd: float) -> "Ply":
        """Environmental knock-down (e.g. wet/aged condition)."""
        return replace(
            self,
            name=f"{self.name} (KD)",
            E1=self.E1 * stiffness_kd, E2=self.E2 * stiffness_kd,
            G12=self.G12 * stiffness_kd,
            Xt=self.Xt * strength_kd, Xc=self.Xc * strength_kd,
            Yt=self.Yt * strength_kd, Yc=self.Yc * strength_kd,
            S=self.S * strength_kd,
        )


LIBRARY = {
    "glass_ud_epoxy": Ply(
        "UD E-glass/epoxy (Vf~0.55)", 40_000, 10_000, 4_000, 0.28,
        1000, 600, 30, 110, 70, 0.25, 1.95, 3.0, 4.0,
        notes="Indicative reference values."),
    "flax_ud_epoxy": Ply(
        "UD flax/epoxy (Vf~0.40)", 30_000, 4_000, 2_000, 0.35,
        300, 130, 25, 90, 40, 0.25, 1.30, 2.0, 9.0,
        moisture_sensitive=True,
        notes="Indicative; flax shows a bilinear tensile response, so E1 "
              "is the initial modulus."),
    "flax_twill_epoxy": Ply(
        "2x2 twill flax/epoxy (Vf~0.40)", 9_500, 9_500, 1_800, 0.10,
        110, 90, 110, 90, 35, 0.30, 1.30, 2.0, 8.0,
        moisture_sensitive=True, notes="Indicative woven ply, balanced."),
}

DEFAULT_KD = {"stiffness": 0.90, "strength": 0.75}  # placeholder wet/aged factors
