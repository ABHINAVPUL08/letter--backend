# Unable to Reach Letter Backend

Generates the Unable to Reach client letter for the Law Office of Jaspreet Singh frontend.

- English letter is always created
- Hindi or Punjabi letter is created from the same template
- Only the client name, A-number, date, and selected office change
- GPT is used to write the client name in Hindi/Punjabi script

## Setup

```powershell
cd c:\Users\abhin\OneDrive\Desktop\backend-letter\letter--backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and paste your OpenAI key:

```
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4o-mini
AUTH_DISABLED=true
PORT=8000
```

Start the API:

```powershell
uvicorn app.main:app --reload --port 8000
```

Check it is running: open http://localhost:8000/health

## Test without the frontend

Keep the server running, then in another terminal:

```powershell
cd c:\Users\abhin\OneDrive\Desktop\backend-letter\letter--backend
.\.venv\Scripts\python.exe scripts\test_api.py
```

That script:

1. Checks http://localhost:8000/health
2. Submits the same JSON the frontend sends
3. Polls `/api/job-status/{job_id}`
4. Downloads the zip to `Downloads\unable_to_reach_test.zip`

Unzip that file and open both Word documents. You should get:

- English letter (always)
- Hindi or Punjabi letter (same layout)
- Only the name and A-number different from the Rohit sample

To test Punjabi, change `"language": "hindi"` to `"language": "punjabi"` in `scripts/test_api.py`.

## Test with the frontend

1. Keep this backend running on port 8000.
2. In `frontend jslo/law-firm-frontend` create or edit `.env`:

```
VITE_API_BASE=http://localhost:8000
```

3. Restart the frontend (`npm run dev`, port 8080).
4. Open http://localhost:8080/unable-to-reach-letter-document
5. Fill Native Language, office, first name, last name, and 9-digit A-number.
6. Click **Generate Unable to Reach Letter**.
7. When it succeeds, download the zip.

The previous `Server error: 404` happened because this endpoint did not exist yet. After the backend is running and `VITE_API_BASE` points to it, that call should return a `job_id`.
