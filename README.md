# vocalsplit
Make your own karaoke from an audio clip

# back-end
This branch will contain the backend final code, ready to merge with main.

# Code workings
To run your FastAPI backend locally and verify that Demucs and all endpoints are functioning correctly, follow these steps:

### Step 1: Set Up a Virtual Environment & Install Dependencies

Open your terminal in the `backend/` directory:

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (Command Prompt / PowerShell):
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

```

> **Note on FFmpeg:** Demucs requires **FFmpeg** to process audio files. Make sure FFmpeg is installed on your system and added to your system PATH. You can check by running `ffmpeg -version`. If you are using Docker, FFmpeg is already included in the Dockerfile.

---

### Step 2: Run the FastAPI Server

Start the application using Uvicorn with hot-reloading enabled:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

You should see output similar to this:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
INFO:     Started server process [...]
INFO:     Waiting background tasks [...]

```

---

### Step 3: Check and Verify the Backend

You can check if everything is running fine through three different methods:

#### 1. Browser Check (Root Endpoint)

Open your browser or run a quick curl command to check the root message:

* **URL:** `http://localhost:8000/`
* **Expected JSON response:**
```json
{"message": "Vocal Remover FastAPI Backend is running."}

```



#### 2. Interactive API Docs (Swagger UI)

FastAPI automatically generates interactive documentation where you can test your endpoints right in the browser:

* **URL:** `http://localhost:8000/docs`
* **What to test:**
* Expand the `POST /upload` endpoint, click **Try it out**, upload a short audio file (`.mp3` or `.wav`), and execute.
* Copy the returned `job_id`.
* Go to `GET /status/{job_id}`, paste the ID, and execute to watch it transition from `queued` $\rightarrow$ `processing` $\rightarrow$ `completed`.
* Once completed, use `GET /download/{job_id}/vocals` or `GET /download/{job_id}/no_vocals` to test downloading your separated audio tracks.



#### 3. Quick Command-Line Health Check

Run this curl command in a separate terminal window to ensure the server responds:

```bash
curl -X 'GET' 'http://localhost:8000/' -H 'accept: application/json'

```

---
