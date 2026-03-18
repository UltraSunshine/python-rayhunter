import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "python-rayhunter"
copyright = "2026, UltraSunshine"
author = "UltraSunshine"
release = "2026.3.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

suppress_warnings = ["autodoc"]

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_rtype = True
napoleon_use_param = True
napoleon_attr_annotations = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = []

html_theme_options = {
    "description": "Unofficial Python bindings for EFF's Rayhunter API",
    "github_user": "UltraSunshine",
    "github_repo": "python-rayhunter",
    "github_banner": True,
    "fixed_sidebar": True,
}
