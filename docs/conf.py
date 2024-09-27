import os
import sys
sys.path.insert(0, os.path.abspath('..'))
print("Python path:", sys.path)

project = 'seekwellpandas'
copyright = '2024, Essi Parent'
author = 'Essi Parent'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

master_doc = 'index'
source_suffix = ['.rst', '.md']
htmlhelp_basename = 'seekwellpandasDoc'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
html_logo = '_images/logo.png'