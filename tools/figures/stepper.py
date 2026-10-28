"""Step-through figure: several SVG frames shown one at a time with previous / next buttons.

    from stepper import stepper
    html = stepper([(svg_1, "caption 1"), (svg_2, "caption 2")], aria="...")

The page gets one line of HTML (a ``div.stepper``); ``docs/javascripts/question-tools.js``
adds the navigation and the site's CSS hides every frame but the active one. Captions are
HTML, so Hebrew text in them is laid out right-to-left like the rest of the page.
"""

import html


def stepper(frames, aria):
    parts = [f'<div class="stepper" role="group" aria-label="{html.escape(aria)}" tabindex="0">']
    for i, (svg, caption) in enumerate(frames):
        active = " is-active" if i == 0 else ""
        parts.append(f'<figure class="stepper-frame{active}">{svg}<figcaption>{caption}</figcaption></figure>')
    parts.append('<div class="stepper-nav">'
                 '<button type="button" class="stepper-btn stepper-prev">הקודם</button>'
                 f'<span class="stepper-pos" data-total="{len(frames)}"></span>'
                 '<button type="button" class="stepper-btn stepper-next">הבא</button>'
                 '</div></div>')
    return "".join(parts)
