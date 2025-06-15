import requests
import json
import time

class VideoEditor:
    def __init__(self, api_key=None):
        # Можно передать ключ явно или прописать здесь
        self.api_key = api_key or "tCXND55PaAJfuunBAFkVAT2r1cH04FkgxxKBec14"
        #self.api_key = api_key or "yqVjXom8wxNuIL0v6uAlloKfG45yr3D9iszde9Qu"

        #self.api_url = "https://api.shotstack.io/v1"
        self.api_url = "https://api.shotstack.io/stage"

        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def create_video_with_subtitle(self, video_url, subtitle_text, duration=5.0):
        data = {
            "timeline": {
                "tracks": [
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "video",
                                    "src": video_url
                                },
                                "start": 0,
                                "length": duration
                            }
                        ]
                    },
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "caption",
                                    "src": subtitle_text,
                                    "font": {
                                        "family": "Open Sans",
                                        "color": "#ffffff",
                                        "opacity": 0.8,
                                        "size": 24,
                                        "lineHeight": 0.85,
                                        "stroke": "#ff6600",
                                        "strokeWidth": 0.8
                                    },
                                    "background": {
                                        "color": "#000000",
                                        "opacity": 0.4,
                                        "padding": 30,
                                        "borderRadius": 18
                                    },
                                    "margin": {
                                        "top": 0.25,
                                        "left": 0.05,
                                        "right": 0.45
                                    },
                                    "trim": 2,
                                    "speed": 1
                                },
                                "start": 0,
                                "length": duration
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
        
        print("Отправляем запрос на рендеринг:")
        print("URL:", f"{self.api_url}/render")
        print("Headers:", json.dumps(self.headers, indent=2))
        print("Data:", json.dumps(data, indent=2))
        
        response = requests.post(f"{self.api_url}/render", headers=self.headers, data=json.dumps(data))
        print("\nПолучен ответ:")
        print("Status code:", response.status_code)
        print("Response:", response.text)
        
        if response.status_code in (200, 201):
            render_id = response.json()["response"]["id"]
            print(f"Рендеринг начат. ID: {render_id}")
            return render_id
        else:
            print(f"Ошибка при создании видео: {response.status_code}\n{response.text}")
            return None

    def check_render_status(self, render_id):
        print(f"\nПроверяем статус рендера {render_id}:")
        response = requests.get(f"{self.api_url}/render/{render_id}", headers=self.headers)
        print("Status code:", response.status_code)
        print("Response:", response.text)
        
        if response.status_code == 200:
            status = response.json()["response"]["status"]
            print(f"Статус рендера: {status}")
            return status
        else:
            print(f"Ошибка при проверке статуса: {response.status_code}\n{response.text}")
            return None

    def wait_for_result_url(self, render_id, poll_interval=5):
        while True:
            response = requests.get(f"{self.api_url}/render/{render_id}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()["response"]
                status = data["status"]
                print(f"Статус: {status}")
                if status == "done":
                    print(f"Ссылка на видео: {data['url']}")
                    return data['url']
                elif status == "failed":
                    print("Рендер не удался.")
                    print("Детали ошибки:", json.dumps(data, indent=2))
                    return None
            else:
                print(f"Ошибка при проверке статуса: {response.status_code}\n{response.text}")
                return None
            time.sleep(poll_interval) 