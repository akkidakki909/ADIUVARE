from .base import RoutePolicy


BUILTIN_POLICIES = {
    "payment": RoutePolicy(sensitivity="critical", ai_mode="assist", sink_mode="inline"),
    "auth": RoutePolicy(sensitivity="critical", ai_mode="off", sink_mode="inline"),
    "admin": RoutePolicy(sensitivity="critical", ai_mode="critical", sink_mode="inline"),
    "search": RoutePolicy(sensitivity="public", ai_mode="off", sink_mode="off"),
}
