import urllib.request
import json

API_KEY = "rnd_WvAGKcUHtU6g30HjZR8NXF6zMs5B"
OWNER_ID = "tea-d0ccuoali9vc73b76k0g"

payload = {
    "type": "web_service",
    "name": "chainbreaker-backend",
    "ownerId": OWNER_ID,
    "repo": "https://github.com/Sekhar-Harshitha/Chainbreaker-AI",
    "autoDeploy": "yes",
    "branch": "main",
    "serviceDetails": {
        "env": "python",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT",
        "region": "singapore",
        "plan": "free",
        "envSpecificDetails": {
            "pythonVersion": "3.10.0"
        }
    }
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.render.com/v1/services",
    data=data,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        print("SUCCESS!")
        service = result.get("service", {})
        print(f"Service Name: {service.get('name')}")
        print(f"Service URL:  https://{service.get('serviceDetails', {}).get('url', 'check render dashboard')}")
        print(f"Service ID:   {service.get('id')}")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP Error {e.code}: {body}")
except Exception as ex:
    print(f"Error: {ex}")
