from flask import Flask, request, jsonify
import os
import uuid
import tempfile
from gtts import gTTS  # You might use a different TTS service in production

app = Flask(__name__)

VOICE_MAPPING = {
    'male1': 'en-us',  # Standard US male
    'female1': 'en',   # Standard female
    'male2': 'en-uk',   # British male
    'female2': 'en-au'  # Australian female
}

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'male1')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    try:
        # Create a temporary file for the audio
        output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp3")
        
        # Generate speech (using gTTS for example)
        tts = gTTS(text=text, lang=VOICE_MAPPING.get(voice, 'en-us'))
        tts.save(output_path)
        
        # Return the path (in production, upload to cloud storage and return URL)
        return jsonify({
            'success': True,
            'audio_path': output_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
