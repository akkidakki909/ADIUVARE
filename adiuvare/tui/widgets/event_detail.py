from textual.widgets import Static


class EventDetail(Static):
    def show_event(self, event: dict | None) -> None:
        if not event:
            self.update("select a row to inspect")
            return

        breakdown = event.get("breakdown") or {}
        detail = event.get("detail") or {}
        lines = [
            f"identity: {event.get('identity', '?')}",
            f"endpoint: {event.get('endpoint', '?')}",
            f"verdict: {event.get('verdict', 'allow')}",
            f"signals: {', '.join(sorted(breakdown)) or 'none'}",
        ]
        ai = detail.get("ai") if isinstance(detail, dict) else None
        if isinstance(ai, dict) and ai:
            lines.append(f"ai verdict: {ai.get('verdict', 'n/a')}")
        note = detail.get("note") if isinstance(detail, dict) else None
        if note:
            lines.append(f"note: {note}")
        self.update("\n".join(lines))

