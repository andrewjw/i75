# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.abspath('extensions'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.pngmath', 'sphinx.ext.ifconfig',
              'epub2', 'mobi', 'autoimage', 'code_example']

todo_include_todos = True
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
#add_module_names = True
# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

project = u'interstate75-wrapper'
copyright = u'2023, Andrew Wilkinson'

version = ''
release = ''

# -- Options for HTML output ---------------------------------------------------

html_theme = 'book'
html_theme_path = ['themes']
html_title = "interstate75-wrapper"
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_show_sphinx = False
htmlhelp_basename = 'interstate75-wrapper'
html_show_sourcelink = False
