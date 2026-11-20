"""Step-through figure: several SVG frames shown one at a time with previous / next buttons.

    from stepper import stepper
    html = stepper([(svg_1, "caption 1"), (svg_2, "caption 2")], aria="...")

The page gets one line of HTML (a ``div.stepper``); ``docs/javascripts/question-tools.js``
adds the navigation. Only the first frame is in the page; every later one is a
``<template>``, outside the document until its step is shown, so a long stepper does not
weigh on the page (the 20 and 30 people circles of 0016 were 3,000 elements, N11.1).
Captions are HTML, so Hebrew text in them is laid out right-to-left like the rest of the
page.
"""

import html


def stepper(frames, aria):
    parts = [f'<div class="stepper" role="group" aria-label="{html.escape(aria)}" tabindex="0">']
    for i, (svg, caption) in enumerate(frames):
        if i == 0:
            parts.append(f'<figure class="stepper-frame is-active">{svg}<figcaption>{caption}</figcaption></figure>')
        else:
            parts.append(f'<template class="stepper-later"><figure class="stepper-frame">{svg}'
                         f'<figcaption>{caption}</figcaption></figure></template>')
    parts.append('<div class="stepper-nav">'
                 '<button type="button" class="stepper-btn stepper-prev">הקודם</button>'
                 f'<span class="stepper-pos" data-total="{len(frames)}"></span>'
                 '<button type="button" class="stepper-btn stepper-next">הבא</button>'
                 '</div></div>')
    return "".join(parts)
