# API для интеграции с n8n

## Запуск API сервера

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
python api.py
```

Сервер будет доступен на `http://localhost:5001`

## Endpoints

### POST /create_video
Создает видео с субтитрами, используя случайное видео из Google Drive

**Параметры запроса (JSON):**
```json
{
    "subtitle_text": "Ваш текст для субтитров"
}
```

**Автоматически:**
- `video_url` - случайное видео из папки Google Drive
- `duration` - автоматически определяется из видео
- `subtitle_file` - создается SRT файл из текста

**Ответ:**
```json
{
    "success": true,
    "render_id": "render_id_here",
    "result_url": "https://cdn.shotstack.io/...",
    "video_url": "https://drive.google.com/uc?export=download&id=...",
    "duration": 15.5,
    "subtitle_text": "Ваш текст для субтитров"
}
```

### GET /health
Проверка состояния сервера

**Ответ:**
```json
{
    "status": "ok"
}
```

## Интеграция с n8n

В n8n используйте HTTP Request node:

1. **Method:** POST
2. **URL:** `http://localhost:5001/create_video`
3. **Headers:** `Content-Type: application/json`
4. **Body (JSON):**
```json
{
    "subtitle_text": "{{ $json.subtitle_text }}"
}
```

## Пример использования в n8n

1. Добавьте HTTP Request node
2. Настройте как показано выше
3. В следующем узле используйте:
   - `{{ $json.result_url }}` - URL готового видео
   - `{{ $json.video_url }}` - URL исходного видео
   - `{{ $json.duration }}` - длительность видео
   - `{{ $json.subtitle_text }}` - исходный текст субтитров

## Особенности

- **Случайное видео**: API автоматически выбирает случайное видео из папки Google Drive
- **Автоматическая длительность**: Длительность определяется автоматически из метаданных видео
- **Карусель**: Каждый вызов использует новое случайное видео
- **Локальные субтитры**: SRT файлы создаются локально, не зависят от внешних ссылок 