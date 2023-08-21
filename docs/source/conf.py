# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
sys.path.insert(0, os.path.abspath('../../src/dataAcquisition'))
sys.path.insert(0, os.path.abspath('../../src/analysis'))
sys.path.insert(0, os.path.abspath('../../src/entropyEstimation'))
sys.path.insert(0, os.path.abspath('../../src/nlp'))
sys.path.insert(0, os.path.abspath('../../src/preprocessing'))


extensions = ['sphinx.ext.autodoc']


project = 'Noisy Entropy Estimation'
copyright = '2023, Siméon Ferez'
author = 'Siméon Ferez'
release = 'V1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'insipid'
html_static_path = ['_static']

html_context = {
    'display_github': True,
    'github_user': 'sferez',
    'github_repo': 'Noisy_Entropy_in_Languages',
}
