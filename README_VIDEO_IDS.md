# Как получить ID видео из Google Drive

## Способ 1: Из URL файла

1. Откройте файл в Google Drive
2. Скопируйте URL из адресной строки
3. URL имеет формат: `https://drive.google.com/file/d/VIDEO_ID/view`
4. Скопируйте `VIDEO_ID` (часть между `/d/` и `/view`)

## Способ 2: Из ссылки для скачивания

1. Правый клик на файле → "Получить ссылку"
2. Скопируйте ссылку
3. Формат: `https://drive.google.com/file/d/VIDEO_ID/view?usp=sharing`
4. Скопируйте `VIDEO_ID`

## Пример

Если у вас есть файлы:
- IMG_8747.MOV
- IMG_8748.MOV
- IMG_8749.MOV

И их ID соответственно:
- 1ABC123
- 1DEF456
- 1GHI789

То в `simple_drive_utils.py` добавьте:

```python
fallback_videos = [
    "https://drive.google.com/uc?export=download&id=1ABC123",
    "https://drive.google.com/uc?export=download&id=1DEF456", 
    "https://drive.google.com/uc?export=download&id=1GHI789"
]
```

## Автоматическое получение ID

Для автоматического получения всех ID из папки можно использовать Google Drive API, но это требует настройки аутентификации. 