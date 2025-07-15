from flask import Flask, request, jsonify
from video_editor import VideoEditor
from simple_drive_utils import get_random_video_from_public_folder, get_video_duration
from subtitle_handler import create_subtitle_file
import os

app = Flask(__name__)

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        data = request.get_json()
        
        # Получаем текст субтитров из webhook
        subtitle_text = data.get('subtitle_text')
        
        if not subtitle_text:
            return jsonify({'error': 'subtitle_text обязателен'}), 400
        
        # Создаем SRT файл из текста
        subtitle_url = create_subtitle_file(subtitle_text)
        
        # Получаем случайное видео из Google Drive
        video_url = get_random_video_from_public_folder()
        
        if not video_url:
            return jsonify({'error': 'Не удалось получить видео из Google Drive'}), 500
        
        # Получаем длительность видео автоматически
        duration = get_video_duration(video_url)
        
        print(f"Используем видео: {video_url}")
        print(f"Длительность: {duration} секунд")
        print(f"Субтитры: {subtitle_text}")
        print(f"Файл субтитров: {subtitle_url}")
        
        # Создаем экземпляр редактора
        editor = VideoEditor()
        
        # Вызываем функцию создания видео
        render_id = editor.create_video_with_subtitle(
            video_url=video_url,
            subtitle_text=subtitle_url,
            duration=duration
        )
        
        if render_id:
            # Ждем результат
            result_url = editor.wait_for_result_url(render_id)
            return jsonify({
                'success': True,
                'render_id': render_id,
                'result_url': result_url,
                'video_url': video_url,
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