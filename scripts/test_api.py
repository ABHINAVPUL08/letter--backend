import json
import time
import urllib.request
from pathlib import Path

print(urllib.request.urlopen("http://127.0.0.1:8000/health").read().decode())
payload = {
    "firstName": "ROHIT",
    "lastName": "KUMAR",
    "clientName": "KUMAR, ROHIT",
    "aNumber": "215509759",
    "language": "hindi",
    "addr_code": "add1",
}
boundary = "----LetterTestBoundary"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="data_json"\r\n\r\n'
    + json.dumps(payload)
    + f"\r\n--{boundary}--\r\n"
).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/unable-to-reach-letter",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST",
)
res = json.loads(urllib.request.urlopen(req).read().decode())
print("submit", res)
job = res["job_id"]
for _ in range(10):
    st = json.loads(
        urllib.request.urlopen(f"http://127.0.0.1:8000/api/job-status/{job}").read().decode()
    )
    print("status", st)
    if st["status"] in ("completed", "failed"):
        break
    time.sleep(0.4)
out = Path.home() / "Downloads" / "unable_to_reach_test.zip"
data = urllib.request.urlopen(f"http://127.0.0.1:8000/api/download/{job}").read()
out.write_bytes(data)
print("downloaded", out, "bytes", len(data))
