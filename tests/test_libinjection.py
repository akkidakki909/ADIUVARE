from pathlib import Path

import adiuvare.vendor._libinjection as libmod

from adiuvare.vendor._libinjection import build_hint, detect_sqli, detect_xss, normalize, source_ready


def test_normalize_decodes_common_wrapper_noise():
    text = "%3Cscript%3Ealert%281%29%3C%2Fscript%3E"
    assert normalize(text) == "<script>alert(1)</script>"


def test_vendor_source_tree_is_restored():
    assert source_ready() is True
    assert (Path(libmod.__file__).with_name("libinjection_src") / "libinjection_sqli_data.h").exists()


def test_build_hint_points_at_local_scripts():
    hint = build_hint()
    assert "scripts/build_libinjection.sh" in hint
    assert "scripts/build_libinjection.py" in hint


def test_detect_sqli_falls_back_when_dll_is_missing(monkeypatch):
    monkeypatch.setattr(libmod, "_load_lib", lambda: None)
    res = detect_sqli("' or 1=1 --")
    assert res["hit"] is True
    assert res["conf"] > 0.0


def test_detect_xss_falls_back_when_dll_is_missing(monkeypatch):
    monkeypatch.setattr(libmod, "_load_lib", lambda: None)
    res = detect_xss("<script>alert(1)</script>")
    assert res["hit"] is True
    assert res["conf"] > 0.0
