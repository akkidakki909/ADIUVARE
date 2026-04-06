import pytest

from adiuvare import Guard


def test_guard_policy_decorator_uses_builtin_bundle():
    guard = Guard()

    @guard.policy("admin")
    async def view():
        return {"ok": True}

    assert view._adiuvare_cfg["ai_mode"] == "critical"
    assert view._adiuvare_cfg["sensitivity"] == "critical"


def test_guard_protect_decorator_sets_inline_cfg():
    guard = Guard()

    @guard.protect(sensitivity="public", ai_mode="assist", trackB=False)
    async def view():
        return {"ok": True}

    assert view._adiuvare_cfg["sensitivity"] == "public"
    assert view._adiuvare_cfg["trackB"] is False


def test_guard_exempt_marks_route():
    guard = Guard()

    @guard.exempt()
    async def view():
        return {"ok": True}

    assert view._adiuvare_exempt is True


def test_guard_policy_rejects_unknown_name():
    guard = Guard()
    with pytest.raises(ValueError):
        guard.policy("made_up")


def test_guard_configure_routes_keeps_mapping():
    guard = Guard()
    guard.configure_routes({"/login": {"policy": "auth"}})
    assert guard._route_cfg["/login"]["policy"] == "auth"
