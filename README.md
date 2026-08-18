# Unable to Reach Letter Backend

One API server plus one PDF job script. The frontend does not change.

- **Server** only POST/GET jobs
- **Script** builds the English + Hindi/Punjabi letter and ZIP

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/unable-to-reach-letter` | Create a job (`data_json` form field) |
| GET | `/api/job-status/{job_id}` | Fetch job status |
| GET | `/api/download/{job_id}` | Download the zip when completed |
| GET | `/health` | Health check |

POST returns `{ "job_id": "...", "status": "queued" }`. The server then starts:

```
python scripts/generate_unable_to_reach.py --job-id <job_id>
```

That script writes Word + PDF into `output/<job_id>/` and marks the job completed.

## Setup

```powershell
cd c:\Users\abhin\OneDrive\Desktop\backend-letter\letter--backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Start the API:

```powershell
uvicorn app.main:app --reload --port 8000
```

Check http://localhost:8000/health

## Test without the frontend

Keep the server running, then in another terminal:

```powershell
cd c:\Users\abhin\OneDrive\Desktop\backend-letter\letter--backend
.\.venv\Scripts\python.exe scripts\test_api.py
```

That script:

1. Checks `/health`
2. POSTs the same JSON the frontend sends
3. Polls `/api/job-status/{job_id}`
4. Downloads `/api/download/{job_id}` to `Downloads\unable_to_reach_test.zip`

To test Punjabi, change `"language": "hindi"` to `"language": "punjabi"` in `scripts/test_api.py`.

## Test with the frontend

1. Keep this backend running on port 8000.
2. In `frontend jslo/law-firm-frontend` set:

```
VITE_API_BASE=http://localhost:8000
```

3. Restart the frontend (`npm run dev`, port 8080).
4. Open http://localhost:8080/unable-to-reach-letter-document
5. Generate the letter and download the zip.
