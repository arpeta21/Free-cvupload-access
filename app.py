import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="TalentBridge Talent Vault")

st.title("TalentBridge Talent Vault")

st.subheader("Candidate Registration")

name = st.text_input("Full Name")
email = st.text_input("Email")
mobile = st.text_input("Mobile Number")
city = st.text_input("City")

designation = st.text_input("Current Designation")
experience = st.number_input("Years of Experience", min_value=0)

qualification = st.selectbox(
    "Highest Qualification",
    ["Graduate", "Post Graduate", "MBA", "B.Tech", "M.Tech", "Other"]
)

position = st.text_input("Position Looking For")

skills = st.text_area("Skills")

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if st.button("Submit Profile"):

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    filepath = ""

    if resume:
        filepath = os.path.join("uploads", resume.name)

        with open(filepath, "wb") as f:
            f.write(resume.getbuffer())

    conn = sqlite3.connect("talentvault.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates
    (
    name,email,mobile,city,
    designation,experience,
    qualification,position,
    skills,resume_path
    )
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """,
    (
    name,email,mobile,city,
    designation,experience,
    qualification,position,
    skills,filepath
    ))

    conn.commit()
    conn.close()

    st.success("Profile Submitted Successfully")