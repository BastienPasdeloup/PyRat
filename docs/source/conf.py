# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Ajouter le chemin vers le module pyrat
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyRat'
copyright = '2025, Bastien Pasdeloup & IMT Atlantique'
author = 'Bastien Pasdeloup'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx"
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
napoleon_include_init_with_doc = True
autodoc_member_order = "bysource"

html_static_path = ['_static']
html_css_files = ["custom.css"]

html_logo = "../../pyrat/gui/drawings/pyrat.png"
html_favicon = "../../pyrat/gui/icon/pyrat.png"
