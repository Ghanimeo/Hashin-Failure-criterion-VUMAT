"""Classical laminate theory and first-ply failure (Tsai-Wu, Hashin 2D)."""
from dataclasses import dataclass
import numpy as np

from .materials import Ply


def q_matrix(p: Ply) -> np.ndarray:
    nu21 = p.nu12 * p.E2 / p.E1
    d = 1 - p.nu12 * nu21
    return np.array([[p.E1 / d, p.nu12 * p.E2 / d, 0],
                     [p.nu12 * p.E2 / d, p.E2 / d, 0],
                     [0, 0, p.G12]])


def _T(theta_deg: float):
    c, s = np.cos(np.radians(theta_deg)), np.sin(np.radians(theta_deg))
    # stress transformation global -> material
    Ts = np.array([[c * c, s * s, 2 * c * s],
                   [s * s, c * c, -2 * c * s],
                   [-c * s, c * s, c * c - s * s]])
    return Ts


def qbar(p: Ply, theta: float) -> np.ndarray:
    Ts = _T(theta)
    R = np.diag([1, 1, 2])
    Te = R @ Ts @ np.linalg.inv(R)  # strain transformation
    return np.linalg.inv(Ts) @ q_matrix(p) @ Te


@dataclass
class Laminate:
    plies: list  # list of (Ply, angle_deg), bottom -> top

    @property
    def thickness(self) -> float:
        return sum(p.t for p, _ in self.plies)

    @property
    def areal_mass(self) -> float:
        """kg/m2."""
        return sum(p.t * p.rho for p, _ in self.plies)  # mm*g/cm3 = kg/m2

    @property
    def co2(self) -> float:
        """kg CO2-eq per m2."""
        return sum(p.t * p.rho * p.co2 for p, _ in self.plies)

    @property
    def cost(self) -> float:
        return sum(p.t * p.rho * p.cost for p, _ in self.plies)

    def z(self):
        h = self.thickness
        z = [-h / 2]
        for p, _ in self.plies:
            z.append(z[-1] + p.t)
        return np.array(z)

    def abd(self):
        z = self.z()
        A = np.zeros((3, 3)); B = np.zeros((3, 3)); D = np.zeros((3, 3))
        for k, (p, th) in enumerate(self.plies):
            Q = qbar(p, th)
            A += Q * (z[k + 1] - z[k])
            B += Q * (z[k + 1] ** 2 - z[k] ** 2) / 2
            D += Q * (z[k + 1] ** 3 - z[k] ** 3) / 3
        return A, B, D

    def response(self, N, M):
        A, B, D = self.abd()
        K = np.block([[A, B], [B, D]])
        sol = np.linalg.solve(K, np.concatenate([N, M]))
        return sol[:3], sol[3:]


def tsai_wu_index(p: Ply, s) -> float:
    """Returns failure index FI (failure at FI >= 1) via strength ratio."""
    s1, s2, t12 = s
    F1 = 1 / p.Xt - 1 / p.Xc; F2 = 1 / p.Yt - 1 / p.Yc
    F11 = 1 / (p.Xt * p.Xc); F22 = 1 / (p.Yt * p.Yc); F66 = 1 / p.S ** 2
    F12 = -0.5 * np.sqrt(F11 * F22)
    a = F11 * s1 ** 2 + F22 * s2 ** 2 + F66 * t12 ** 2 + 2 * F12 * s1 * s2
    b = F1 * s1 + F2 * s2
    if a <= 0 and b <= 0:
        return 0.0
    if a <= 1e-30:
        return b
    R = (-b + np.sqrt(b * b + 4 * a)) / (2 * a)  # strength ratio
    return 1 / R


def hashin_index(p: Ply, s) -> tuple:
    """2D Hashin (1980), returns (max index, mode)."""
    s1, s2, t12 = s
    modes = {
        "fibre tension": (s1 / p.Xt) ** 2 + (t12 / p.S) ** 2 if s1 >= 0 else 0,
        "fibre compression": (s1 / p.Xc) ** 2 if s1 < 0 else 0,
        "matrix tension": (s2 / p.Yt) ** 2 + (t12 / p.S) ** 2 if s2 >= 0 else 0,
        "matrix compression": ((s2 / (2 * p.S)) ** 2 + ((p.Yc / (2 * p.S)) ** 2 - 1) * s2 / p.Yc
                               + (t12 / p.S) ** 2) if s2 < 0 else 0,
    }
    mode = max(modes, key=modes.get)
    # quadratic indices -> linear-load index via sqrt where applicable
    return float(np.sqrt(max(modes[mode], 0))), mode


def first_ply_failure(lam: Laminate, N, M):
    """Max failure indices over all plies (top/bottom of each ply)."""
    e0, k = lam.response(np.asarray(N, float), np.asarray(M, float))
    z = lam.z()
    worst = {"tsai_wu": 0.0, "hashin": 0.0, "hashin_mode": "-", "ply": None}
    for i, (p, th) in enumerate(lam.plies):
        for zz in (z[i], z[i + 1]):
            eps = e0 + zz * k
            sig_g = qbar(p, th) @ eps
            sig_m = _T(th) @ sig_g
            tw = tsai_wu_index(p, sig_m)
            hi, mode = hashin_index(p, sig_m)
            if tw > worst["tsai_wu"]:
                worst["tsai_wu"] = tw; worst["ply"] = i
            if hi > worst["hashin"]:
                worst["hashin"] = hi; worst["hashin_mode"] = f"{mode} (ply {i}, {th:g} deg)"
    return worst
