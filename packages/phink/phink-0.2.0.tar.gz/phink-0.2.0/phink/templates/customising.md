# Customising

## Editing Existing Pages

To change a page, simply edit the markdown files in the `{data.doc_path}/` directory.

## Adding New Pages

To add a new page of documentation:

 * Add a new Markdown file to the `{data.doc_path}/` directory.
 * In the `{data.doc_path}/index.rst` file, add the filename to the `toctree` section (without the `.md` extension).

## Sphinx Configuration

The `phlink init` command generates a sample `{data.doc_path}/conf.py` Sphinx configuration file.
You can customise this to your liking - see the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html) for full details.

