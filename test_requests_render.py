import requests
import json

API_KEY = "tCXND55PaAJfuunBAFkVAT2r1cH04FkgxxKBec14"
url = "https://api.shotstack.io/stage/render"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "timeline": {
        "tracks": [
            {
                "clips": [
                    {
                        "asset": {
                            "type": "video",
                            "src": "https://github.com/shotstack/test-media/raw/main/captioning/scott-ko.mp4"
                        },
                        "start": 0,
                        "length": 4
                    },
                    {
                        "asset": {
                            "type": "title",
                            "text": "Это тестовый виральный заголовок, сгенерированный автоматически",
                            "style": "minimal",
                            "size": "medium",
                            "position": "top"
                        },
                        "start": 0,
                        "length": 4
                    }
                ]
            }
        ]
    },
    "output": {
        "format": "mp4",
        "resolution": "mobile"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.text) 