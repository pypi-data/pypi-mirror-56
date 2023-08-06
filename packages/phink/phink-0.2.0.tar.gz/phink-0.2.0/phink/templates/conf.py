# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ------------------------------------------------

project = "{data.project}"

extensions = ["sphinx.ext.napoleon", "recommonmark"]

master_doc = "index"
source_suffix = [".rst", ".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_rtd_theme"
html_show_copyright = False
napoleon_use_rtype = False


def setup(app):
    from recommonmark.transform import AutoStructify

    app.add_config_value("recommonmark_config", {{"enable_eval_rst": True}}, True)
    app.add_transform(AutoStructify)
