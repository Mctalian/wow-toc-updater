#!/usr/bin/env python3
"""Build script to create a bundled distribution with dependencies."""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def get_dependencies():
    """Parse dependencies from pyproject.toml."""
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})

    # Filter out python version requirement and convert to pip format
    pip_deps = []
    for dep, version in dependencies.items():
        if dep == "python":
            continue

        # Handle simple version strings like "^2.31.0"
        if isinstance(version, str):
            # Convert poetry version syntax to pip syntax
            if version.startswith("^"):
                # ^2.31.0 becomes >=2.31.0
                pip_deps.append(f"{dep}>={version[1:]}")
            elif version.startswith("~"):
                # ~2.31.0 becomes >=2.31.0,<2.32.0
                base_version = version[1:]
                pip_deps.append(f"{dep}>={base_version}")
            else:
                # Exact version or other format
                pip_deps.append(f"{dep}{version}")
        else:
            # Handle complex dependency specs (dict format)
            pip_deps.append(dep)

    return pip_deps


def build_bundle():
    """Create a bundled distribution with dependencies."""

    print("🛠️  Building bundled distribution...\n")

    dist_dir = Path("dist")
    if dist_dir.exists():
        print("[+] Cleaning existing dist directory...")
        shutil.rmtree(dist_dir)

    dist_dir.mkdir()

    # Copy source code
    print("[+] Copying source code...")
    shutil.copytree("toc_interface_updater", dist_dir / "toc_interface_updater")

    # Copy license file
    shutil.copy("LICENSE", dist_dir / "LICENSE")

    # Install dependencies to dist/lib
    print("[+] Installing dependencies...")
    lib_dir = dist_dir / "lib"

    # Get dependencies from pyproject.toml
    dependencies = get_dependencies()
    print(f"[++] Found dependencies: {', '.join(dependencies)}")

    if dependencies:
        print("[++] Installing...")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "--target",
                str(lib_dir),
                *dependencies,
            ],
            check=True,
        )
    else:
        print("[++] No dependencies found to install.")
        lib_dir.mkdir()  # Create empty lib directory

    # Create runner script
    print("[+] Creating runner script...")
    runner_content = '''#!/usr/bin/env python3
"""Runner script for the bundled TOC interface updater."""

import sys
import os

# Add bundled dependencies to path
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, "lib")
sys.path.insert(0, lib_dir)

# Import and run main
from toc_interface_updater.cli import main

if __name__ == "__main__":
    main()
'''

    runner_path = dist_dir / "run.py"
    with open(runner_path, "w") as f:
        f.write(runner_content)

    # Make executable
    os.chmod(runner_path, 0o755)

    # Create a requirements file for reference
    dependencies = get_dependencies()
    requirements_content = "# Dependencies bundled in lib/\n"
    if dependencies:
        requirements_content += "\n".join(dependencies) + "\n"
    else:
        requirements_content += "# No dependencies found\n"

    with open(dist_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)

    # Create a README for the dist
    readme_content = """# Bundled Distribution

This directory contains a self-contained bundle of the TOC interface updater
with all its dependencies.

## Usage

```bash
python3 run.py [options]
```

## Contents

- `run.py` - Main entry point script
- `toc_interface_updater/` - Source code
- `lib/` - Bundled Python dependencies
- `requirements.txt` - List of bundled dependencies

This bundle is designed to work on GitHub Actions runners without requiring
additional package installation.
"""

    with open(dist_dir / "README.md", "w") as f:
        f.write(readme_content)

    print(f"\n✅ Bundle created successfully in {dist_dir}/")
    print(f"📁 Contents:")
    for item in sorted(dist_dir.iterdir()):
        if item.is_dir():
            print(f"   📂 {item.name}/")
        else:
            print(f"   📄 {item.name}")


if __name__ == "__main__":
    build_bundle()
