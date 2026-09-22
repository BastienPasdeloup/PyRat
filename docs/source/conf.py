# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath("../../pyrat/workspace"))
sys.path.insert(0, os.path.abspath("../../pyrat/workspace/pyrat_workspace/games"))
sys.path.insert(0, os.path.abspath("../../pyrat/workspace/pyrat_workspace/players"))

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
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton"
]

# Do not copy prompts and outputs when using the copy button on code blocks
copybutton_exclude = ".linenos, .gp, .go"

templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
napoleon_include_init_with_doc = True
autodoc_member_order = "bysource"

# Classes are documented under the name students import them with (e.g. "Game" rather than "pyrat.src.game.game.Game")
add_module_names = False

html_static_path = ['_static']
html_css_files = ["custom.css"]
html_js_files = ["diagram_zoom.js"]

# A role to insert raw HTML inline, used for the links that must open in a new tab (the diagrams at full size)
rst_prolog = """
.. role:: raw-html(raw)
   :format: html
"""

html_logo = "../../pyrat/gui/drawings/pyrat.png"
html_favicon = "../../pyrat/gui/icon/pyrat.png"

# Link to the sources and to the package, shown at the bottom of the left sidebar
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/BastienPasdeloup/PyRat",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}
