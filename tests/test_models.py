from adiuvare.core.models import AdiuvareEvent


def test_adiuvare_event_holds_score_breakdown():
    event = AdiuvareEvent(
        identity="u1",
        endpoint="/login",
        score=0.42,
        verdict="flag",
        breakdown={"payload": 0.28, "identity": 0.14},
    )

    assert event.verdict == "flag"
    assert event.breakdown["payload"] == 0.28
