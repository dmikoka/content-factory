import random
import requests

def get_random_video_from_public_folder():
    """Получает случайное видео из публичной папки Google Drive"""
    
    # Список ID видеофайлов из папки
    # ID можно получить из URL файлов в Google Drive
    video_ids = [
        "1SxtecPFLJdH-G-Le64P_YeKiZ6qMAcFD",
        "1JOw6vvD0xwiTkHiCyjwuNFfyoMyfKsz1",
        "1LigSEN76ZhLlpp_uSYUe3AGwDv7vORoP",
        "1WDWbd6Tx9wm0_krqupwjUJLlQ-r2bTs6",
        "1_1mz0cxVBSh71laxva4uqmFeknrczm_t",
        "1IhrFF1auKCzh8818xhOkw1HWjDUgYjFp",
        "1HbjvfDrlubEU9NZxxCsHahOnMwcE9aRx",
        "1EBtLq2WNTK3hbM4FGDtjKirXbPYz0Ym9",
        "1xfFDmClf6_Ye482DAH-5R7mB6TivPirH",
        "1wX38j3XvfFPiM-R9cO5l5kun0jeUFTHU",
        "1XrxeoehxvCSXaT_AQaH6irM4YJ3sKyaH",
        "1SxN3XnRPotkSC4jOdF6FWuFtJtmHu8fk",
        "1kpahzanwrCXB14A-UxkKmcpl23GtccqN",
        "1G84cBehjxjOfSm55kAp-_arzqsjp2xLY",
        "1HwyD1It8GSvYE2QmiPDQ8mOPWXXcc_bk"
    ]
    
    # Создаем список прямых ссылок на видео
    video_urls = [
        f"https://drive.google.com/uc?export=download&id={video_id}"
        for video_id in video_ids
    ]
    
    # Пытаемся получить случайное видео
    try:
        # Выбираем случайное видео из списка
        video_url = random.choice(video_urls)
        print(f"Выбрано случайное видео: {video_url}")
        return video_url
    except Exception as e:
        print(f"Ошибка при выборе видео: {e}")
        return video_urls[0] if video_urls else None

def get_video_duration(video_url):
    """Получает длительность видео через Shotstack API"""
    try:
        import os
        # Используем Shotstack API для получения метаданных видео
        api_key = os.getenv('SHOTSTACK_API_KEY')
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "url": video_url
        }
        
        response = requests.post(
            "https://api.shotstack.io/stage/inspect",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            duration = result.get('response', {}).get('duration', 5.0)
            print(f"Длительность видео: {duration} секунд")
            return duration
        else:
            print(f"Не удалось получить длительность видео: {response.status_code}")
            return 5.0  # значение по умолчанию
            
    except Exception as e:
        print(f"Ошибка при получении длительности видео: {e}")
        return 5.0  # значение по умолчанию 