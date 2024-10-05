# frontend/auth.py
import streamlit as st
import pyrebase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


# Function for user login
def login(email, password):
    try:
        # First, try to sign in the user
        user = auth.sign_in_with_email_and_password(email, password)

        # Now, check if the user exists in the Realtime Database
        user_data = firebase.database().child("users").child(email.replace('.', ',')).get()
        if user_data.val() is None:
            st.error("User does not exist in the database. Please sign up first.")
            return None

        # Validate the password against the database (if stored)
        stored_password = user_data.val().get("password")
        if stored_password == password:
            return user
        else:
            st.error("Incorrect password.")
            return None

    except:
        st.error(f"Login failed! Please try again.")


# Function for user signup
def sign_up(email, password):
    try:
        # Check if the user already exists
        user_data = firebase.database().child("users").child(email.replace('.', ',')).get()
        if user_data.val() is not None:
            st.error("User already exists. Please log in.")
            return

        # Create the user in Firebase Auth
        auth.create_user_with_email_and_password(email, password)

        # Store the user data in the Realtime Database
        firebase.database().child("users").child(email.replace('.', ',')).set({
            "password": password
        })
        st.success("Sign-up successful! You can now log in.")
    except:
        st.error(f"Password must be 6 characters long. Please try again.")
