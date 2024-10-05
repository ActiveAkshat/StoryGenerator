import time
import streamlit as st
from frontend.authentication import login, sign_up
from frontend.landingpage import showLandingPage

# Streamlit UI

# Initialize session state to check if splash screen has been shown
if 'splash_shown' not in st.session_state:
    st.session_state['splash_shown'] = False

# Splash screen logic
if not st.session_state['splash_shown']:
    # Display splash screen with logo and app name
    st.markdown("<h1 style='text-align: center;'>📚StoryGPT</h1>", unsafe_allow_html=True)
    st.spinner("Loading...")

    # Wait for 1 seconds
    time.sleep(1)

    # Mark splash screen as shown
    st.session_state['splash_shown'] = True

    # Force rerun to move to login page
    st.rerun()

if 'user' not in st.session_state:
    # Login form
    st.set_page_config(page_title="StoryGPT Login", page_icon="📚")
    st.title("📚 Story GPT")
    st.header("Login")
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state['user'] = user
            st.success("Logged in successfully!")
            time.sleep(2)
            st.rerun()

    # Sign up form
    st.header("Or Sign Up")
    if st.button("Sign Up"):
        sign_up(email, password)

else:
    # Logged-in user section
    showLandingPage()
