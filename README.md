# Content Factory

Проект для автоматизации создания видео с субтитрами с использованием Shotstack API.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/content-factory.git
cd content-factory
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

1. Получите API ключ от Shotstack (https://shotstack.io/)

2. Создайте файл `.env` и добавьте ваш API ключ:
```
SHOTSTACK_API_KEY=your_api_key_here
```

3. Запустите тестовый скрипт:
```bash
python test_video.py
```

## Структура проекта

- `video_editor.py` - основной класс для работы с видео
- `test_video.py` - пример использования
- `requirements.txt` - зависимости проекта

## Требования

- Python 3.9+
- Shotstack API ключ 