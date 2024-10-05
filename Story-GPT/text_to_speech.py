# texttospeech.py

import requests

CHUNK_SIZE = 1024
def text_to_speech_elevenlabs(text, voice_id, api_key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        audio_path = 'output.mp3'
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        return audio_path  # Return the path to the generated audio file
    else:
        print(f"Error: {response.status_code}, {response.text}")  # Debugging output
        return None
