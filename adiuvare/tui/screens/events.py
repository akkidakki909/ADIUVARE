from typing import cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Input, Static

from ..widgets.event_detail import EventDetail
from ..workspace import WorkspaceView


class EventsScreen(WorkspaceView):
    shortcut_hints = "[1-6] tabs  [/] filter  [c] confirm  [u] whitelist  [n] note"
    primary_id = "events-table"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rows: list[dict] = []
        self._selected: dict | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Input(placeholder="identity filter", id="events-identity-filter")
                yield Button("Confirm", id="events-confirm")
                yield Button("Whitelist", id="events-whitelist")
                yield Button("Note", id="events-note")
            with Horizontal(id="events-shell"):
                with Vertical(classes="monitor-main"):
                    yield DataTable(id="events-table")
                with Vertical(classes="monitor-side"):
                    yield EventDetail(id="events-detail")
                    yield Input(placeholder="optional note", id="events-note-input")
                    yield Static("", id="events-summary")

    def on_mount(self) -> None:
        table = self.query_one("#events-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("verdict", "identity", "endpoint")
        self.refresh_view()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "events-identity-filter":
            self.refresh_view()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if 0 <= event.cursor_row < len(self._rows):
            self._selected = self._rows[event.cursor_row]
            self.query_one("#events-detail", EventDetail).show_event(self._selected)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self._selected:
            return
        who = str(self._selected.get("identity", ""))
        if event.button.id == "events-confirm":
            self._app().confirm_identity(who)
            self._app().set_footer_status("confirm marker recorded")
        elif event.button.id == "events-whitelist":
            self._app().whitelist_identity(who)
            self._app().set_footer_status("whitelist marker recorded")
        elif event.button.id == "events-note":
            note = self.query_one("#events-note-input", Input).value.strip()
            self._app().mark_note(who, note)
            self._app().set_footer_status("review note saved")

    def refresh_view(self) -> None:
        filt = self.query_one("#events-identity-filter", Input).value.strip().lower()
        rows = [row for row in self._app().recent_rows(60) if str(row.get("verdict", "allow")) != "allow"]
        if filt:
            rows = [row for row in rows if filt in str(row.get("identity", "")).lower()]
        self._rows = rows
        table = self.query_one("#events-table", DataTable)
        table.clear(columns=False)
        for row in rows:
            table.add_row(
                str(row.get("verdict", "allow")),
                str(row.get("identity", "?"))[:20],
                str(row.get("endpoint", "?"))[:26],
            )
        self._selected = rows[0] if rows else None
        self.query_one("#events-detail", EventDetail).show_event(self._selected)
        self.query_one("#events-summary", Static).update(f"showing {len(rows)} reviewable rows")

    def footer_status(self) -> str:
        if self._selected:
            return f"selected: {self._selected.get('identity', '?')}"
        return "review queue is quiet"

    def _app(self):
        return cast("AdiuvareApp", self.app)

