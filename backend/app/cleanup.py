import time
from pathlib import Path

OUTPUTS_DIR = Path("storage/outputs")
UPLOADS_DIR = Path("storage/uploads")

def cleanup_old_files(max_age_seconds: int = 86400):
    """Deletes files older than 24 hours."""
    now = time.time()
    for directory in [OUTPUTS_DIR, UPLOADS_DIR]:
        if not directory.exists():
            continue
        for item in directory.glob("*"):
            if item.is_dir():
                # Check directory age
                if now - item.stat().st_mtime > max_age_seconds:
                    for sub in item.glob("**/*"):
                        if sub.is_file():
                            sub.unlink()
                    try:
                        item.rmdir()
                    except OSError:
                        pass
            elif item.is_file():
                if now - item.stat().st_mtime > max_age_seconds:
                    item.unlink()