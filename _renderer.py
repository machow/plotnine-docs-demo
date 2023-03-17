from __future__ import annotations

import html
from importlib.resources import files
from quartodoc import MdRenderer
from quartodoc.renderers.base import convert_rst_link_to_md
from quartodoc import layout
from plum import dispatch
from typing import Union

from griffe import dataclasses as dc
from griffe.docstrings import dataclasses as ds

from pathlib import Path


P_ROOT = Path(__file__).parent
EXAMPLES_FOLDER = P_ROOT / "plotnine-examples/plotnine_examples"

DOCSTRING_TMPL = """\
{rendered}

Examples
--------

{examples}
"""


class Renderer(MdRenderer):
    style = "plotnine"

    @dispatch
    def render(self, el: layout.DocClass):
        return super().render(el)

    @dispatch
    def render(self, el: Union[dc.Object, dc.Alias]):
        rendered = super().render(el)

        converted = convert_rst_link_to_md(rendered)

        p_example = EXAMPLES_FOLDER / "examples" / (el.name + ".ipynb")
        if p_example.exists():
            rel_path = Path("..") / p_example.relative_to(P_ROOT)
            example = f"{{{{< embed {rel_path} >}}}}"
            return DOCSTRING_TMPL.format(rendered=converted, examples=example)

        return converted

    def render_annotation(self, el: dc.Name | dc.Expression | None):
        return super().render_annotation(el)

    @dispatch
    def summarize(self, el: dc.Object | dc.Alias):
        result = super().summarize(el)
        return html.escape(result)

    


