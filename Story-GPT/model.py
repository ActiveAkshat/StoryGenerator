from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import requests

from text_to_speech import text_to_speech_elevenlabs

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)


@st.cache_resource
def initialize_llm():
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)


def generate_content(topic):
    try:
        story_model = genai.GenerativeModel(model_name="tunedModels/socialstories-my8gxcmyb2vx")
        image_prompt_model = genai.GenerativeModel(model_name="tunedModels/imagepromptsgeneration-n56rok7p5r5v")

        story_session = story_model.start_chat(history=[])
        image_prompt_session = image_prompt_model.start_chat(history=[])

        story = story_session.send_message(f"Generate a social story on topic {topic}").text
        image_prompt = image_prompt_session.send_message(story).text

        audio = text_to_speech_elevenlabs(
            story,
            voice_id="your_voice_id",  # Replace with your ElevenLabs voice ID
            api_key="your_elevenlabs_api_key"  # Replace with your ElevenLabs API key
        )

        if not story or not image_prompt:
            return None  # Return None if something is missing

        return {
            'story': story,
            'story_list': get_story_list(story),
            'image_prompt': image_prompt,
            'audio': audio
        }

    except Exception as e:
        print(f"Error generating content: {e}")
        return None  # Return None if something goes wrong


def get_story_list(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]
    n = len(sentences) // 2
    return [" ".join(sentences[:n]), " ".join(sentences[n:])]

def texttospeech():

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "<xi-api-key>"
    }

    data = {
        "text": "Born and raised in the charming south,I can add a touch of sweet southern hospitality to your audiobooks and podcasts","model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
