"""mapgen: recipe-driven map building (docs/DESIGN_mapgen.md).

A recipe (``*.map.yaml``, coordinates in feet) is an ordered list of GIMP-like
operations on named layers. The engine runs it deterministically and writes a
PNG, a Universal VTT file and a meta.json.
"""
__all__ = ["render"]


def render(*args, **kwargs):
    """Render a recipe. See :func:`mapgen.export.render_recipe`."""
    from .export import render_recipe
    return render_recipe(*args, **kwargs)
