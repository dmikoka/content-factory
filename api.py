from flask import Flask, request, jsonify
from video_editor import VideoEditor
from simple_drive_utils import get_random_video_from_public_folder, get_video_duration
from subtitle_handler import create_subtitle_file
import os
from pyairtable import Api as AirtableApi
from dotenv import load_dotenv
import random

load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

def get_user_assets_from_airtable(webhook_id):
    api = AirtableApi(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    row = table.first(formula=f"{{webhook_id}}='{webhook_id}'")
    if row:
        fields = row['fields']
        video_samples = fields.get('video_samples', [])
        audio_tracks = fields.get('audio_tracks', [])
        return video_samples, audio_tracks
    return [], []

app = Flask(__name__)

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        data = request.get_json()
        webhook_id = data.get('webhook_id')
        print('webhook_id:', webhook_id)
        subtitle_text = data.get('subtitle_text')
        if not subtitle_text:
            return jsonify({'error': 'subtitle_text обязателен'}), 400
        if not webhook_id:
            return jsonify({'error': 'webhook_id обязателен'}), 400
        # Получаем пул видео и аудио из Airtable
        video_samples, audio_tracks = get_user_assets_from_airtable(webhook_id)
        if not video_samples:
            return jsonify({'error': 'Нет доступных видео-семплов для этого пользователя'}), 400
        video_url = random.choice(video_samples)
        audio_url = random.choice(audio_tracks) if audio_tracks else None
        # Создаем SRT файл из текста
        subtitle_url = create_subtitle_file(subtitle_text)
        # Получаем длительность видео автоматически
        duration = get_video_duration(video_url)
        print(f"Используем видео: {video_url}")
        print(f"Длительность: {duration} секунд")
        print(f"Субтитры: {subtitle_text}")
        print(f"Файл субтитров: {subtitle_url}")
        editor = VideoEditor()
        # Генерируем видео с/без аудио
        render_id = editor.create_video_with_subtitle(
            video_url=video_url,
            subtitle_text=subtitle_url,
            duration=duration,
            audio_url=audio_url
        )
        if render_id:
            result_url = editor.wait_for_result_url(render_id)
            return jsonify({
                'success': True,
                'render_id': render_id,
                'result_url': result_url,
                'video_url': video_url,
                'audio_url': audio_url,
                'duration': duration,
                'subtitle_text': subtitle_text
            })
        else:
            return jsonify({'error': 'Не удалось создать видео'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 