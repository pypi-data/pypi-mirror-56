#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))
from templot import __version__  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_gallery.gen_gallery',
    'sphinx_rtd_theme',
    'matplotlib.sphinxext.plot_directive',
]

templates_path = ['_templates']
html_logo = '_static/logo.svg'
source_suffix = '.rst'
master_doc = 'index'
project = 'templot'
copyright = '2019'
author = 'Khalil Kacem'
version = __version__
release = __version__
language = 'en'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True

import sphinx_rtd_theme  # noqa
html_theme = "sphinx_rtd_theme"

html_theme_options = {}
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

htmlhelp_basename = 'templot_doc'
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc,
     'templot.tex',
     'templot\\_unit\\_test\\_ci Documentation',
     'Khalil Kacem',
     'manual'),
]

texinfo_documents = [
    (master_doc, 'templot', 'templot Documentation',
     author, 'templot', 'Python package for visualizing temporal evolution.',
     'Miscellaneous'),
]

intersphinx_mapping = {'https://docs.python.org/': None}

sphinx_gallery_conf = {
    # path to your examples scripts
    'examples_dirs': '../examples',
    # path where to save gallery generated examples
    'gallery_dirs': 'examples'
}
