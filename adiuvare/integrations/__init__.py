from ..core.models import RequestContext


def build_http_ctx(
    *,
    identity: str,
    payload: str | None,
    url: str,
    method: str,
    headers: dict,
    ip: str,
    endpoint: str,
    snapshot,
) -> RequestContext:
    return RequestContext(
        identity=identity,
        payload=payload,
        url=url,
        method=method,
        headers=headers,
        ip=ip,
        endpoint=endpoint,
        snapshot=snapshot,
    )
