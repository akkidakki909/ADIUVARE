from pathlib import Path


class ConfigWatcher:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._stamp = self._mtime()

    def check(self) -> bool:
        stamp = self._mtime()
        if stamp <= self._stamp:
            return False
        self._stamp = stamp
        return True

    def _mtime(self) -> float:
        if not self.path.exists():
            return 0.0
        return self.path.stat().st_mtime

