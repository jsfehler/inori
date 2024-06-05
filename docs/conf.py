# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

import inori
from inori import *

# -- Project information -----------------------------------------------------

project = 'inori'
copyright = '2021, Joshua Fehler'
author = 'Joshua Fehler'

# The full version, including alpha/beta/rc tags
version = inori.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_immaterial',
]

napoleon_use_param = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_immaterial'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    "repo_url": "https://github.com/jsfehler/inori",
    "repo_name": "inori",
    "icon": {
        "repo": "fontawesome/brands/git",
        "edit": "material/file-edit-outline",
    },
    "font": False,
    "features": [
        "navigation.expand",
        "navigation.sections",
        "navigation.top",
        "navigation.tracking",
        "search.share",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "blue-grey",
            "accent": "orange",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "grey",
            "accent": "amber",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],

}
