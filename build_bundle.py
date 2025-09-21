import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def parse_dependencies():
    """Parse dependencies from pyproject.toml."""
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    dependencies = pyproject["tool"]["poetry"]["dependencies"]

    # Filter out python version constraint and convert to pip format
    deps = []
    for name, constraint in dependencies.items():
        if name != "python":
            if isinstance(constraint, str):
                # Convert Poetry version syntax to pip syntax
                if constraint.startswith("^"):
                    # ^2.31.0 becomes >=2.31.0
                    version = constraint[1:]
                    deps.append(f"{name}>={version}")
                elif constraint.startswith("~"):
                    # ~2.31.0 becomes >=2.31.0,<2.32.0 (compatible release)
                    version = constraint[1:]
                    deps.append(f"{name}~={version}")
                elif (
                    constraint.startswith(">=")
                    or constraint.startswith("<=")
                    or constraint.startswith("==")
                    or constraint.startswith("!=")
                    or constraint.startswith(">")
                    or constraint.startswith("<")
                ):
                    # Already in pip format
                    deps.append(f"{name}{constraint}")
                else:
                    # Assume exact version if no operator
                    deps.append(f"{name}=={constraint}")
            elif isinstance(constraint, dict):
                # Handle complex dependency specifications
                # For now, just use the package name and let pip resolve
                deps.append(name)

    return deps


def clean_platform_specific_files(lib_dir):
    """Remove platform-specific files that cause diff issues."""

    # Remove bin directory entirely - we don't need console scripts
    bin_dir = lib_dir / "bin"
    if bin_dir.exists():
        shutil.rmtree(bin_dir)

    # Clean up RECORD files that contain absolute paths and hashes of bin files
    for record_file in lib_dir.glob("**/*.dist-info/RECORD"):
        if record_file.exists():
            lines = []
            with open(record_file, "r") as f:
                for line in f:
                    # Skip lines that reference the bin directory
                    if not line.startswith("../../bin/"):
                        lines.append(line)

            with open(record_file, "w") as f:
                f.writelines(lines)


def build_bundle():
    """Create a bundled distribution with dependencies."""

    print("🔨 Building bundled distribution...")

    dist_dir = Path("dist")
    if dist_dir.exists():
        print("🧹 Cleaning existing dist directory...")
        shutil.rmtree(dist_dir)

    dist_dir.mkdir()

    # Copy source code
    print("📦 Copying source code...")
    shutil.copytree("toc_interface_updater", dist_dir / "toc_interface_updater")

    # Copy LICENSE file
    print("📄 Copying LICENSE file...")
    shutil.copy("LICENSE", dist_dir / "LICENSE")

    # Parse dependencies from pyproject.toml
    print("📋 Parsing dependencies from pyproject.toml...")
    dependencies = parse_dependencies()

    # Install dependencies to dist/lib
    if dependencies:
        print(f"📥 Installing dependencies: {', '.join(dependencies)}")
        lib_dir = dist_dir / "lib"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "--target",
                str(lib_dir),
                "--no-deps",  # Don't install sub-dependencies automatically
                *dependencies,
            ],
            check=True,
        )

        # Install sub-dependencies separately to ensure we get everything
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "--target",
                str(lib_dir),
                "--upgrade",  # Force upgrade to handle any conflicts
                *dependencies,
            ],
            check=True,
        )

        # Clean platform-specific files
        print("🧽 Cleaning platform-specific files...")
        clean_platform_specific_files(lib_dir)

    # Create requirements.txt for reference
    print("📝 Creating requirements.txt...")
    requirements_content = (
        "\n".join(dependencies) + "\n" if dependencies else "# No dependencies\n"
    )
    with open(dist_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)

    # Create runner script
    print("🏃 Creating runner script...")
    runner_content = '''#!/usr/bin/env python3
"""
Bundled runner for toc-interface-updater GitHub Action.
This script includes all dependencies and can run standalone.
"""
import sys
import os

# Add bundled dependencies to path
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, "lib")
if os.path.exists(lib_dir):
    sys.path.insert(0, lib_dir)

# Import and run main
try:
    from toc_interface_updater.cli import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing toc_interface_updater: {e}")
    print("Make sure the bundle was built correctly.")
    sys.exit(1)
'''

    runner_path = dist_dir / "run.py"
    with open(runner_path, "w") as f:
        f.write(runner_content)

    # Make executable
    os.chmod(runner_path, 0o755)

    # Create README for the dist directory
    readme_content = """# Bundled Distribution

This directory contains a self-contained bundle of the toc-interface-updater
for use in GitHub Actions.

## Contents

- `run.py` - Main executable script
- `toc_interface_updater/` - Source code
- `lib/` - Bundled dependencies  
- `requirements.txt` - List of bundled dependencies

## Usage

```bash
python3 run.py --help
```

This bundle is automatically generated by `build_bundle.py` and should not be
manually edited.
"""

    with open(dist_dir / "README.md", "w") as f:
        f.write(readme_content)

    print("✅ Bundle created successfully in dist/")

    # Show contents
    print("📁 Contents:")
    for item in sorted(dist_dir.iterdir()):
        if item.is_dir():
            print(f"   📂 {item.name}/")
        else:
            print(f"   📄 {item.name}")


if __name__ == "__main__":
    build_bundle()
