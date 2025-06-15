from video_editor import VideoEditor
import os

if __name__ == "__main__":
    editor = VideoEditor()
    render_id = editor.create_video_with_subtitle(
        video_url="https://github.com/shotstack/test-media/raw/main/captioning/scott-ko.mp4",
        subtitle_text="https://shotstack-assets.s3.amazonaws.com/captions/transcript.srt",
        duration=10.0 # длительность видео из примера документации
    )
    print("Render ID:", render_id)
    if render_id:
        editor.wait_for_result_url(render_id)
    