import os
import base64
import requests
from datetime import datetime
import time

GITHUB_USER = os.getenv('GITHUB_USER')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_SUBS_PATH = os.getenv('GITHUB_SUBS_PATH')

class SubtitleHandler:
    def __init__(self):
        self.subtitles_dir = "subtitles"
        self.ensure_subtitles_dir()
    
    def ensure_subtitles_dir(self):
        """Создает директорию для субтитров если её нет"""
        if not os.path.exists(self.subtitles_dir):
            os.makedirs(self.subtitles_dir)
    
    def create_srt_from_text(self, text, filename=None):
        """Создает SRT файл из текста"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"subtitle_{timestamp}.srt"
        
        filepath = os.path.join(self.subtitles_dir, filename)
        
        # Создаем простой SRT файл
        srt_content = f"""1
00:00:00,000 --> 00:00:05,000
{text}

2
00:00:05,000 --> 00:00:10,000
{text}

3
00:00:10,000 --> 00:00:15,000
{text}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        print(f"Создан SRT файл: {filepath}")
        return filepath, filename
    
    def wait_for_github_file(self, url, timeout=120):
        print(f"Ожидание появления файла по ссылке: {url}")
        start = time.time()
        while time.time() - start < timeout:
            try:
                r = requests.head(url)
                print(f"HEAD {url} -> {r.status_code}")
                if r.status_code == 200:
                    print(f"Файл стал доступен по ссылке: {url}")
                    return True
            except Exception as ex:
                print(f"Ошибка HEAD-запроса: {ex}")
            time.sleep(2)
        print(f"Файл не появился на GitHub за {timeout} секунд: {url}")
        return False

    def upload_to_github(self, filepath, filename):
        """Загружает файл в GitHub"""
        print(f"Пробую загрузить {filename} в {GITHUB_REPO}/{GITHUB_SUBS_PATH}")
        with open(filepath, 'rb') as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode('utf-8')
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_SUBS_PATH}/{filename}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "message": f"Add subtitle {filename}",
            "content": b64_content
        }
        print(f"PUT {api_url}")
        response = requests.put(api_url, headers=headers, json=data)
        print(f"Ответ GitHub: {response.status_code} {response.text}")
        if response.status_code in (200, 201):
            print(f"Файл {filename} успешно загружен на GitHub.")
            raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/content-factory/main/{GITHUB_SUBS_PATH}/{filename}"
            # Ждем появления файла по raw-ссылке
            ok = self.wait_for_github_file(raw_url, timeout=60)
            print(f"wait_for_github_file вернул: {ok}")
            if ok:
                return raw_url
            else:
                print("Файл не появился вовремя, возвращаю None.")
                return None
        else:
            print(f"Ошибка загрузки на GitHub: {response.status_code} {response.text}")
            return None
    
    def get_subtitle_url(self, text):
        """Основная функция для получения ссылки на субтитры"""
        try:
            filepath, filename = self.create_srt_from_text(text)
            subtitle_url = self.upload_to_github(filepath, filename)
            print(f"upload_to_github вернул: {subtitle_url}")
            if subtitle_url:
                print(f"Ссылка на субтитры: {subtitle_url}")
                return subtitle_url
            else:
                print("Использую fallback, т.к. subtitle_url = None")
                raise Exception("Не удалось загрузить файл на GitHub или дождаться его появления")
        except Exception as e:
            print(f"Ошибка при создании субтитров: {e}")
            return "https://raw.githubusercontent.com/dmikoka/content-factory/refs/heads/main/subtitles.srt"

def create_subtitle_file(text):
    """Упрощенная функция для создания субтитров"""
    handler = SubtitleHandler()
    return handler.get_subtitle_url(text) 