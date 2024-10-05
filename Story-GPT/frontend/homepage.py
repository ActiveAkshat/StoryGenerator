import streamlit as st
from model import generate_content
from generate_image import generate_image
from text_to_speech import text_to_speech_elevenlabs

# Initialize session state for user_topic, story_output, generated_image, and audio if they don't exist
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'audio' not in st.session_state:
    st.session_state.audio = None  # Initialize audio in session state

# Streamlit UI Home Page
st.title("📚 Story GPT")
st.write("Enter a topic, and I'll generate a social story, a split version, an image prompt, and convert the story to speech for you!")

# User input
st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

if st.button("Generate Story"):
    if st.session_state.user_topic:
        with st.spinner("Generating story and image ..."):
            # Generate story content
            result = generate_content(st.session_state.user_topic)
            if result and result['story'] != '':
                st.session_state.story_output = result  # Store output in session state
                st.success("Story generated!")

                st.write(f"### Full Story\n{st.session_state.story_output['story']}")
                st.write(f"### Story in Parts\n1. {st.session_state.story_output['story_list'][0]}")
                st.write(f"2. {st.session_state.story_output['story_list'][1]}")
                st.write(f"### Image Prompt\n{st.session_state.story_output['image_prompt']}")

                # Placeholder for the image (before generating)
                image_placeholder = st.empty()
                image_placeholder.image("frontend/assets/loading-placeholder.png", caption="Generating Image...", width=300)

                # Generate and display the image
                image_prompt = result['image_prompt']
                generated_img = generate_image(f"{image_prompt}")

                # Once image is ready, replace the placeholder
                if generated_img:
                    st.session_state.generated_image = generated_img  # Store the image in session state
                    image_placeholder.image(generated_img, caption="Generated Image", width=300)

            else:
                st.warning('Topic may be explicit or invalid.')
    else:
        st.warning("Please enter a topic.")

# Button for generating and playing the audio
if st.session_state.story_output:
    if st.button("Convert to Audio"):
        with st.spinner("Converting story to speech..."):
            st.session_state.audio = text_to_speech_elevenlabs(
                st.session_state.story_output['story'],
                voice_id="your_voice_id",  # Replace with your voice ID
                api_key="your_elevenlabs_api_key"  # Replace with your ElevenLabs API key
            )

            # Debugging output
            if st.session_state.audio:
                st.success("Audio successfully generated!")
                st.audio(st.session_state.audio, format="audio/mp3")
            else:
                st.warning("Audio conversion failed. Please check your inputs.")
