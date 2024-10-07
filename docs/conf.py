import os
import sys

# Ajoute le répertoire parent au chemin Python
sys.path.insert(0, os.path.abspath('..'))
print("Python path:", sys.path)

# Information sur le projet
project = 'seekwellpandas'
copyright = '2024, Essi Parent'
author = 'Essi Parent'
release = '0.2.5'

# Extensions Sphinx
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Configuration de base
master_doc = 'index'
source_suffix = ['.rst', '.md']

# Configuration de la sortie
htmlhelp_basename = 'seekwellpandasDoc'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Thème et style
html_theme = 'alabaster'
html_static_path = ['_static']
html_logo = '_static/logo.png'

# Assurez-vous que ces chemins sont corrects
source_dir = 'source'
html_extra_path = ['_static']

# Configuration supplémentaire
autodoc_member_order = 'bysource'
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Configuration pour intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}