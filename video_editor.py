import requests
import json
import time
import os
from dotenv import load_dotenv

class VideoEditor:
    def __init__(self, api_key=None):
        load_dotenv()  # загружаем переменные из .env
        self.api_key = api_key or os.getenv('SHOTSTACK_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set SHOTSTACK_API_KEY in .env file or pass it to constructor")

        # self.api_url = "https://api.shotstack.io/v1" #production
        self.api_url = "https://api.shotstack.io/stage" #stage

        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def create_video_with_subtitle(self, video_url, subtitle_text, duration=5.0, audio_url=None):   
        data = {
            "timeline": {
                "tracks": [
                    # Слой субтитров
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "caption",
                                    "src": subtitle_text,
                                    "width": 900,
                                    "font": {
                                        "size": 45,
                                        "color": "#ffffff"
                                    },
                                    "alignment": {
                                        "horizontal": "center"
                                    }
                                },
                                "start": 0,
                                "length": "end",
                                "position": "center"
                            }
                        ]
                    },
                    # Слой PNG-подложки
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "image",
                                    "src": "https://raw.githubusercontent.com/dmikoka/content-factory/main/video_effects/IMG_9464.PNG"
                                },
                                "start": 0,
                                "length": "end",
                                "position": "top"
                            }
                        ]
                    },
                    # Слой видео
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "video",
                                    "src": video_url
                                },
                                "start": 0,
                                "length": duration,
                                "transform": {
                                    "rotate": {"angle": 0}
                                }
                            }
                        ]
                    }
                ]
            },
            "output": {
                "format": "mp4",
                "size": {
                    "width": 1080,
                    "height": 1920
                }
            }
        }
        # Добавляем аудиотрек, если есть
        if audio_url:
            data["timeline"]["tracks"].append({
                "clips": [
                    {
                        "asset": {
                            "type": "audio",
                            "src": audio_url
                        },
                        "start": 0,
                        "length": "end"
                    }
                ]
            })
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