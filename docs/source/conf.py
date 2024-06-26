# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ScrutinyCSPM'
copyright = '2024, Robert Fischer, Daniel Healy, Eric Margolis, Gregory Frasco'
author = '2024, Robert Fischer, Daniel Healy, Eric Margolis, Gregory Frasco'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc','autoapi.extension']
autoapi_dirs = ['../../src']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# For Sphinx to find the source code
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))