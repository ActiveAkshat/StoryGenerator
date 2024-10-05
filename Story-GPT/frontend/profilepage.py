import streamlit as st
import time

# Fetch user email from session state
if 'user' in st.session_state:
    user_email = st.session_state['user']['email']
else:
    st.warning("You need to log in to view your profile.")
    st.stop()

# Check if username exists and set title accordingly
if 'username' in st.session_state and st.session_state['username']:
    title = f"Hello, {st.session_state['username']}!"
else:
    title = ":material/account_circle: Hello, User!"

st.title(title)

email_icon = ':material/mail:'
st.write(f"{email_icon} Email: {user_email}")

# Input for username
username = st.text_input("Username", placeholder="Enter your username", value=st.session_state.get('username', ''))

# Button to save or edit username
if st.button("Save Username"):
    if username:
        # Save username logic (e.g., update in database)
        st.session_state['username'] = username  # Store username in session state
        st.success(f"Username '{username}' saved successfully!")
        time.sleep(1)
        st.rerun()  # Rerun the page to show updated username
    else:
        st.warning("Please enter a username.")

# Logout button
if st.button("Logout"):
    # Clear user session and redirect to login page
    del st.session_state['user']
    st.session_state['logged_out'] = True
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()  # This will redirect to the login page
