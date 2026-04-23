from textual.widgets import Static

from ..workspace import PALETTE, decision_color


class SignalChart(Static):
    def show_breakdown(self, breakdown: dict[str, float]) -> None:
        if not breakdown:
            self.update("no signal pressure yet")
            return

        peak = max(breakdown.values()) or 1.0
        rows = []
        for name, value in sorted(breakdown.items(), key=lambda item: item[1], reverse=True):
            blocks = int((value / peak) * 16)
            rows.append(
                f"{name:<10} "
                f"[{decision_color('flag')}]{'#' * blocks}[/{decision_color('flag')}] "
                f"[{PALETTE['dim']}]{value:0.2f}[/{PALETTE['dim']}]"
            )
        self.update("\n".join(rows))

