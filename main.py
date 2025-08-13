from flask import Flask, request, jsonify
import os
import uuid
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import tempfile

app = Flask(__name__)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    data = request.main.py
    text = data.get('text')
    style = data.get('style', 'professional')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    try:
        # Create a temporary file for the video
        output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp4")
        
        # Create text clip (in a real app, you'd have more sophisticated generation)
        txt_clip = TextClip(text, fontsize=24, color='white', size=(640, 480))
        txt_clip = txt_clip.set_duration(10)  # 10 second duration
        
        # Create background based on style
        if style == 'professional':
            bg_color = '#6c5ce7'
        elif style == 'animated':
            bg_color = '#a29bfe'
        elif style == 'minimal':
            bg_color = '#ffffff'
        else:  # cinematic
            bg_color = '#2d3436'
            
        # Create final video
        video = CompositeVideoClip([txt_clip.set_position('center')], size=(640, 480))
        video = video.set_bgcolor(bg_color)
        
        # Write the video file
        video.write_videofile(output_path, fps=24)
        
        # Return the path (in production, upload to cloud storage and return URL)
        return jsonify({
            'success': True,
            'video_path': output_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
