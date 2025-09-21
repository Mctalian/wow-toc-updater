"""Type definitions and enums for the TOC interface updater."""

from enum import Enum
from typing import Dict, Literal

# Product type definitions
TestProduct = Literal["wowt", "wowxptr", "wow_classic_ptr", "wow_classic_era_ptr"]
BetaProduct = Literal["wow_beta", "wow_classic_beta", "wow_classic_era_beta"]
FullProduct = Literal["wow", "wow_classic", "wow_classic_era"]
Product = TestProduct | BetaProduct | FullProduct
VersionCache = Dict[Product, str]


class GameFlavor(Enum):
    """Enumeration of supported WoW game flavors."""

    WOW = "wow"
    WOW_CLASSIC = "wow_classic"
    WOW_CLASSIC_ERA = "wow_classic_era"
