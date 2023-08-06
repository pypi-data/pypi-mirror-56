"""
Template tags loaded in by the Django
templating engine when {% load django_simple_buefy %}
is called.
"""

from pathlib import Path

from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe

from django_simple_buefy.constants import (
    BUEFY,
    BUEFY_ESM,
    BUEFY_ESM_MIN,
    BUEFY_MIN,
    VUE_FULL,
    VUE_FULL_ESM,
    VUE_FULL_ESM_MIN,
    VUE_FULL_MIN,
)

register = template.Library()
simple_buefy_path = Path(__file__).resolve().parent.parent

js_folder: Path = simple_buefy_path / "js"
component_folder: Path = js_folder / "components"
component_folder_esm: Path = js_folder / "esm"

try:
    BUEFY_SETTINGS = settings.BUEFY_SETTINGS
except AttributeError:
    BUEFY_SETTINGS = {}

DEBUG = BUEFY_SETTINGS.get("debug", False)
MODULES = BUEFY_SETTINGS.get("modules", True)


@register.simple_tag
def buefy():
    """
    Build and return all the HTML required to import buefy, bulma and vue.
    """

    # Build the html to include the stylesheet
    css = static("css/buefy.css")
    html = [f'  <link rel="stylesheet" href="{css}">']

    if DEBUG:
        if MODULES is None:
            buefy_js = tuple(js_folder / x for x in BUEFY) + tuple(js_folder / x for x in BUEFY_ESM)
            vue_js = tuple(js_folder / x for x in VUE_FULL) + tuple(
                js_folder / x for x in VUE_FULL_ESM
            )
        elif MODULES:
            buefy_js = tuple(js_folder / x for x in BUEFY_ESM)
            vue_js = tuple(js_folder / x for x in VUE_FULL_ESM)
        else:
            buefy_js = tuple(js_folder / x for x in BUEFY)
            vue_js = tuple(js_folder / x for x in VUE_FULL)
    else:
        if MODULES is None:
            buefy_js = tuple(js_folder / x for x in BUEFY_MIN) + tuple(
                js_folder / x for x in BUEFY_ESM_MIN
            )
            vue_js = tuple(js_folder / x for x in VUE_FULL_MIN) + tuple(
                js_folder / x for x in VUE_FULL_ESM_MIN
            )
        elif MODULES:
            buefy_js = tuple(js_folder / x for x in BUEFY_ESM_MIN)
            vue_js = tuple(js_folder / x for x in VUE_FULL_ESM_MIN)
        else:
            buefy_js = tuple(js_folder / x for x in BUEFY_MIN)
            vue_js = tuple(js_folder / x for x in VUE_FULL_MIN)

    base_js = vue_js + buefy_js

    if MODULES:
        components = component_folder_esm
    else:
        components = component_folder

    # Build html to include all the js files required.
    for filename in base_js:
        js_file = static(f"js/{filename.name}")

        if "esm" in str(filename):
            html.append(f'  <script type="module" src="{js_file}"></script>')
        elif MODULES is None:
            html.append(f'  <script nomodule type="text/javascript" src="{js_file}"></script>')
        else:
            html.append(f'  <script type="text/javascript" src="{js_file}"></script>')

    for filename in components.iterdir():
        js_file = static(f"js/{filename.relative_to(js_folder)}")

        if "esm" in str(filename):
            html.append(f'  <script type="module" src="{js_file}"></script>')
        elif MODULES is None:
            html.append(
                f'  <script nomodule type="text/javascript" src="{js_file}/index.js"></script>'
            )
        else:
            html.append(f'  <script type="text/javascript" src="{js_file}/index.js"></script>')

    return mark_safe("\n".join(html))  # noqa
