import threading
from typing import Dict, Any

class JobManager:
    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_job(self, job_id: str) -> None:
        with self._lock:
            self._jobs[job_id] = {
                "status": "queued",
                "output_dir": None,
                "error": None
            }

    def update_job(self, job_id: str, status: str, output_dir: str = None, error: str = None) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = status
                if output_dir:
                    self._jobs[job_id]["output_dir"] = output_dir
                if error:
                    self._jobs[job_id]["error"] = error

    def get_job(self, job_id: str) -> dict:
        with self._lock:
            return self._jobs.get(job_id)

job_manager = JobManager()