import os
import sys

# Add the src/ directory to the path so autodoc can find the rayhunter package
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

project = "python-rayhunter"
copyright = "2025, UltraSunshine"
author = "UltraSunshine"
release = "2025.3.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# autodoc settings
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

# napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]

html_theme_options = {
    "description": "Unofficial Python bindings for EFF's Rayhunter API",
    "github_user": "jmg292",
    "github_repo": "python-rayhunter",
    "fixed_sidebar": True,
}
