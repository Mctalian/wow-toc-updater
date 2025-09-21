"""Battle.net API client for fetching version information."""

import requests

from .types import Product, VersionCache


def product_version(product: Product, version_cache: VersionCache) -> str:
    """Fetch version information for a product from Battle.net API."""
    if product in version_cache:
        return version_cache[product]
    else:
        url = f"https://us.version.battle.net/v2/products/{product}/versions"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            response_data = response.text
        except requests.RequestException as e:
            print(f"Error communicating with server: {e}")
            return "00000"

        version = ""
        for line in response_data.splitlines():
            if line.startswith("us"):
                version = line.split("|")[5]
                break
        version = version.rsplit(".", 1)[0]

        [major, minor, patch] = version.split(".")
        # Pad minor and patch to ensure they are two digits
        minor = minor.zfill(2)  # Ensure minor is 2 digits
        patch = patch.zfill(2)  # Ensure patch is 2 digits

        version = f"{major}{minor}{patch}"
        version_cache[product] = version
        return version
