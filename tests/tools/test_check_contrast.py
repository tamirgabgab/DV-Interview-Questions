"""tools/check_contrast.py: the colour parser against known values (hex, rgba, hsla with
Material's hue, color-mix with transparent), the WCAG ratio at its two ends, and the site's
pairs passing in both schemes."""

import pytest

import check_contrast as cc


def close(a, b, eps=1 / 255):
    return all(abs(x - y) <= eps for x, y in zip(a, b))


def test_parse():
    assert close(cc.parse("#1b2a4a"), (27 / 255, 42 / 255, 74 / 255, 1))
    assert close(cc.parse("#0000008a"), (0, 0, 0, 0x8A / 255))
    assert close(cc.parse("#fff"), (1, 1, 1, 1))
    assert close(cc.parse("rgba(217, 154, 0, 0.12)"), (217 / 255, 154 / 255, 0, 0.12))
    assert close(cc.parse("hsla(225deg,15%,14%,1)"), cc.parse("#1e212a"))
    # 7% of a colour into transparent is that colour at 7% opacity
    assert close(cc.parse("color-mix(in srgb, #1f4e9c 7%, transparent)"), (0x1F / 255, 0x4E / 255, 0x9C / 255, 0.07))
    assert close(cc.parse("color-mix(in srgb, #ffffff 50%, #000000)"), (0.5, 0.5, 0.5, 1))
    with pytest.raises(ValueError):
        cc.parse("papayawhip")


def test_resolve_and_ratio():
    props = {"--a": "var(--b)", "--b": "#000"}
    assert cc.resolve("var(--a)", props) == "#000"
    assert cc.resolve("var(--missing, #fff)", props) == "#fff"
    assert round(cc.ratio((0, 0, 0, 1), (1, 1, 1, 1)), 2) == 21.0
    assert cc.ratio((0.5, 0.5, 0.5, 1), (0.5, 0.5, 0.5, 1)) == 1.0
    # black at half opacity over white is mid grey
    assert close(cc.over((0, 0, 0, 0.5), (1, 1, 1, 1)), (0.5, 0.5, 0.5, 1))


def test_the_site_passes(capsys):
    assert cc.check() == 0, capsys.readouterr().out
