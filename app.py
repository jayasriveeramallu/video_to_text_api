from flask import Flask, request, jsonify
import assemblyai as aai
import tempfile
from moviepy.editor import VideoFileClip

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os 
# Set your AssemblyAI API key
aai.settings.api_key=os.getenv('API_KEY')

transcriber = aai.Transcriber()

def extract_audio_from_video(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

@app.route('/', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        # Get raw video data from the POST request
        video_data = request.data

        # Set up audio stream parameters
        fs = 44100  # Sample rate

        # Save video data to a temporary MP4 file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
            video_path = temp_video_file.name
            with open(video_path, 'wb') as vf:
                vf.write(video_data)

            # Extract audio from the video
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                audio_path = temp_audio_file.name
                extract_audio_from_video(video_path, audio_path)

        # Transcribe audio from the temporary file
        transcript = transcriber.transcribe(audio_path)

        # Return the transcription as JSON
        return jsonify({'transcription': transcript.text})

if __name__ == '__main__':
    app.run(debug=True)
