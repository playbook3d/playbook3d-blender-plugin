# toml_compat.py
import sys, os

try:
    # on Python 3.11+ use stdlib
    import tomllib as toml
except ImportError:
    # otherwise prepend your bundled toml/ folder
    addon_dir = os.path.dirname(__file__)
    pkg = os.path.join(addon_dir, "toml")
    if pkg not in sys.path:
        sys.path.insert(0, pkg)
    import toml

# ensure any `import toml` later hits our copy:
sys.modules["toml"] = toml

