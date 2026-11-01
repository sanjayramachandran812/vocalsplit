import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.jobs import job_manager
from app.separator import UPLOADS_DIR, run_demucs

router = APIRouter()

def process_audio_task(job_id: str, file_path: Path):
    try:
        job_manager.update_job(job_id, "processing")
        stems_dir = run_demucs(job_id, file_path)
        job_manager.update_job(job_id, "completed", output_dir=str(stems_dir))
    except Exception as e:
        job_manager.update_job(job_id, "failed", error=str(e))
    finally:
        # Clean up original upload to save space
        if file_path.exists():
            file_path.unlink()

@router.post("/upload")
async def upload_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    allowed_extensions = {".mp3", ".wav", ".flac", ".m4a", ".ogg"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}")

    job_id = str(uuid.uuid4())
    job_manager.create_job(job_id)

    destination = UPLOADS_DIR / f"{job_id}{file_ext}"
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Kick off separation in background thread so the client doesn't timeout
    background_tasks.add_task(process_audio_task, job_id, destination)

    return {"job_id": job_id, "status": "queued"}

@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/download/{job_id}/{stem_type}")
async def download_stem(job_id: str, stem_type: str):
    """
    stem_type can be 'vocals' or 'no_vocals' (instrumental)
    """
    if stem_type not in ["vocals", "no_vocals"]:
        raise HTTPException(status_code=400, detail="Invalid stem type. Choose 'vocals' or 'no_vocals'.")

    job = job_manager.get_job(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job is not completed or does not exist.")

    stems_dir = Path(job["output_dir"])
    file_path = stems_dir / f"{stem_type}.wav"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Requested stem file not found.")

    return FileResponse(path=file_path, filename=f"{stem_id_format(job_id)}_{stem_type}.wav", media_type="audio/wav")

def stem_id_format(job_id: str) -> str:
    return job_id[:8]