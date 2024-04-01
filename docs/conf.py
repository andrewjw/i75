# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.abspath('extensions'))
sys.path.insert(0, os.path.normpath(os.path.dirname(__file__) + os.path.sep + ".."))
sys.path.insert(0, os.path.join(os.path.normpath(os.path.dirname(__file__)), "..", "i75", "emulated", "screens"))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.ifconfig', 'sphinx_rtd_theme']

todo_include_todos = True
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
#add_module_names = True
# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

project = u'i75'
copyright = u'2023-2024, Andrew Wilkinson'

version = ''
release = ''

# -- Options for HTML output ---------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_path = ['themes']
html_title = "i75"
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_show_sphinx = False
htmlhelp_basename = 'i75'
html_show_sourcelink = False
