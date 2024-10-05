import streamlit as st

title_icon = ':material/contact_page:'
st.title(f"{title_icon} Contact Developers")

# Developer details
developers = [
    {"name": "Mohit Vaidya     ", "email": "2022.mohit.vaidya@ves.ac.in"},
    {"name": "Tanmay Maity     ", "email": "2022.tanmay.maity@ves.ac.in"},
    {"name": "Akshat Mahajan   ", "email": "2022.akshat.mahajan@ves.ac.in"},
    {"name": "Sarang Pavanaskar", "email": "2022.sarang.pavanaskar@ves.ac.in"}
]

name_icon = ':material/person:'
email_icon = ':material/mail:'

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

for dev in developers:
    with col1:
        st.write(f"{name_icon} {dev['name']}")
    with col2:
        st.write(f"{email_icon} {dev['email']}")

# Feedback form
st.header("We Value Your Feedback!")
feedback = st.text_input("Please provide your feedback here:")

if st.button("Send Feedback"):
    if feedback:
        st.success("Feedback sent! Thank you for your input.")
        # Here you could add logic to send the feedback to a database or an email
    else:
        st.warning("Please enter your feedback before submitting.")
