from video_editor import VideoEditor
import os

if __name__ == "__main__":
    editor = VideoEditor()
    render_id = editor.create_video_with_subtitle(
        video_url="https://drive.google.com/uc?export=download&id=1SxtecPFLJdH-G-Le64P_YeKiZ6qMAcFD",
        #subtitle_text="https://shotstack-assets.s3.amazonaws.com/captions/transcript.srt",
        subtitle_text="https://raw.githubusercontent.com/dmikoka/content-factory/refs/heads/main/subtitles.srt?token=GHSAT0AAAAAADFWHWFRZC6264UQLVCKALNY2CQAU6A",
        duration=4.0  # длительность видео из примера документации
    )
    print("Render ID:", render_id)
    if render_id:
        editor.wait_for_result_url(render_id)
    