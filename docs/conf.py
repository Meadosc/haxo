"""sphinx config."""
from datetime import datetime

project = "haxo"
author = "rahul"
master_doc = 'index'
copyright = f"2020, {author}"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
html_static_path = ["_static"]
