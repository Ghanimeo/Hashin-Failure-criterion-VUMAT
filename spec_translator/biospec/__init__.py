"""Bio-Composite Spec Translator: glass -> flax / hybrid laminate substitution (screening tool)."""
from .materials import Ply, LIBRARY, DEFAULT_KD
from .clt import Laminate, first_ply_failure
from .translator import Requirement, translate, best

__version__ = "0.1.0"
