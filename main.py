from pathlib import Path
from datetime import datetime
import traceback


def _write_bootstrap_error(exc: BaseException) -> None:
    """把启动阶段异常写入本地日志，方便打包版排查。"""
    candidates = [
        Path.home() / "Desktop",
        Path.cwd(),
    ]
    log_dir = next((p for p in candidates if p.exists()), Path.cwd())
    log_path = log_dir / f"PDFToWordConverter_bootstrap_{datetime.now():%Y%m%d}.log"
    log_path.write_text(
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        encoding="utf-8",
    )


try:
    from src.gui import main as gui_main
except Exception as exc:
    _write_bootstrap_error(exc)
    raise


if __name__ == "__main__":
    try:
        gui_main()
    except Exception as exc:
        _write_bootstrap_error(exc)
        raise
