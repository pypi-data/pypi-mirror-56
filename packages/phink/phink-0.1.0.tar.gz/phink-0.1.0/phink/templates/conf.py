# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = "{data.project}"

extensions = ["sphinx.ext.napoleon", "recommonmark"]

master_doc = "index"
source_suffix = [".rst", ".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_show_copyright = False
napoleon_use_rtype = False


def setup(app):
    from recommonmark.transform import AutoStructify

    app.add_config_value("recommonmark_config", {{"enable_eval_rst": True}}, True)
    app.add_transform(AutoStructify)
