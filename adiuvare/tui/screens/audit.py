import json
from pathlib import Path
from typing import cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Input, Static

from ..widgets.event_detail import EventDetail
from ..workspace import WorkspaceView


class AuditScreen(WorkspaceView):
    shortcut_hints = "[1-6] tabs  [/] filter  [e] export  [r] refresh"
    primary_id = "audit-table"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rows: list[dict] = []
        self._selected: dict | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Input(placeholder="identity filter", id="audit-identity-filter")
                yield Button("Export", id="audit-export")
            with Horizontal(id="audit-shell"):
                with Vertical(classes="monitor-main"):
                    yield DataTable(id="audit-table")
                with Vertical(classes="monitor-side"):
                    yield EventDetail(id="audit-detail")
                    yield Static("", id="audit-summary")

    def on_mount(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("verdict", "identity", "endpoint")
        self.refresh_view()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "audit-identity-filter":
            self.refresh_view()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "audit-export":
            self.action_export_jsonl()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if 0 <= event.cursor_row < len(self._rows):
            self._selected = self._rows[event.cursor_row]
            self.query_one("#audit-detail", EventDetail).show_event(self._selected)

    def action_export_jsonl(self) -> None:
        out = Path("adiuvare_audit_export.jsonl")
        out.write_text("\n".join(json.dumps(row) for row in self._rows), encoding="utf-8")
        self._app().set_footer_status(f"exported {out.name}")

    def refresh_view(self) -> None:
        filt = self.query_one("#audit-identity-filter", Input).value.strip().lower()
        rows = self._app().recent_rows(80)
        if filt:
            rows = [row for row in rows if filt in str(row.get("identity", "")).lower()]
        self._rows = rows
        table = self.query_one("#audit-table", DataTable)
        table.clear(columns=False)
        for row in rows:
            table.add_row(
                str(row.get("verdict", "allow")),
                str(row.get("identity", "?"))[:20],
                str(row.get("endpoint", "?"))[:26],
            )
        self._selected = rows[0] if rows else None
        self.query_one("#audit-detail", EventDetail).show_event(self._selected)
        self.query_one("#audit-summary", Static).update(f"showing {len(rows)} audit rows")

    def _app(self):
        return cast("AdiuvareApp", self.app)
