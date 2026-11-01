import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

API_KEY = os.getenv("DATA_GOV_API_KEY", "").strip()

API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

if not API_KEY:
    print("API KEY NOT FOUND")
else:
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1
    }

    url = API_URL + "?" + urlencode(params)

    req = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

            print("SUCCESS!")
            print("Status:", response.status)
            print("Records:", data.get("records", []))

    except HTTPError as e:
        print("HTTP ERROR:", e.code)
        print("SERVER MESSAGE:", e.read().decode("utf-8", errors="replace"))

    except URLError as e:
        print("CONNECTION ERROR:", e.reason)

    except Exception as e:
        print("OTHER ERROR:", str(e))