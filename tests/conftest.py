import pytest


@pytest.fixture
def toc_files(tmp_path):
    # Import centralized directives
    from toc_interface_updater.constants import InterfaceDirective, TocSuffix

    toc_content = {
        "default.toc": f"{InterfaceDirective.BASE} 110007\n\nfile.lua\n",
        f"specific-{TocSuffix.CLASSIC}.toc": f"{InterfaceDirective.BASE} 40401\n\nfile.lua\n",
        "multi.toc": f"{InterfaceDirective.BASE} 110007\n{InterfaceDirective.VANILLA} 11505\n{InterfaceDirective.CLASSIC} 40401\n{InterfaceDirective.CURRENT_CLASSIC} 40400\n\nfile.lua\n",
        "multi-oneline.toc": f"{InterfaceDirective.BASE} 11505, 40401, 110007\n\nfile.lua\n",
        f"specific-{TocSuffix.MAINLINE}.toc": f"{InterfaceDirective.BASE} 110007\n\nfile.lua\n",
        f"specific_{TocSuffix.CURRENT_CLASSIC}.toc": f"{InterfaceDirective.BASE} 40401\n\nfile.lua\n",
    }

    for filename, content in toc_content.items():
        file_path = tmp_path / filename
        file_path.write_text(content)

    return tmp_path


@pytest.fixture
def product_versions():
    from toc_interface_updater.version_client import product_version

    versions = {}
    product_version("wow", versions)
    product_version("wowt", versions)
    product_version("wowxptr", versions)
    product_version("wow_beta", versions)
    product_version("wow_classic", versions)
    product_version("wow_classic_ptr", versions)
    product_version("wow_classic_beta", versions)
    product_version("wow_classic_era", versions)
    product_version("wow_classic_era_ptr", versions)
    # The product exists but there is no version information for it
    # product_version("wow_classic_era_beta", versions)

    return versions
