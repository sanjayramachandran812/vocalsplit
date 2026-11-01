import os
import subprocess
from pathlib import Path

STORAGE_DIR = Path("storage")
UPLOADS_DIR = STORAGE_DIR / "uploads"
OUTPUTS_DIR = STORAGE_DIR / "outputs"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def run_demucs(job_id: str, input_file_path: Path) -> Path:
    """
    Runs Demucs to separate audio into 2 stems (vocals and instrumental/no_vocals).
    """
    job_output_dir = OUTPUTS_DIR / job_id
    job_output_dir.mkdir(parents=True, exist_ok=True)

    # Command line invocation of demucs ensures reliable memory management and GPU/CPU device handling
    # -n htdemucs: uses the standard high-performance model
    # --two-stems vocals: extracts specifically 'vocals' and 'no_vocals'
    command = [
        "demucs",
        "-n", "htdemucs",
        "--two-stems", "vocals",
        "-o", str(job_output_dir),
        str(input_file_path)
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Demucs processing failed: {e.stderr}")

    # Demucs saves output under <job_output_dir>/htdemucs/<track_name>/
    track_name = input_file_path.stem
    stems_dir = job_output_dir / "htdemucs" / track_name
    
    if not stems_dir.exists():
        raise FileNotFoundError(f"Expected output stems directory not found at {stems_dir}")

    return stems_dir