import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Employer Portal")

st.title("🏢 TalentBridge Talent Vault")
st.subheader("Employer Portal")

# Login
password = st.text_input(
    "Employer Access Code",
    type="password"
)

if password == "talentbridge123":

    st.success("Access Granted")

    # Database Connection
    conn = sqlite3.connect("talentvault.db")

    # Load Data
    df = pd.read_sql_query("""
    SELECT
        id,
        name,
        city,
        designation,
        experience,
        qualification,
        position,
        skills,
        resume_path
    FROM candidates
    """, conn)

    conn.close()

    if len(df) == 0:
        st.info("No candidate profiles available.")
        st.stop()

    # Filters
    st.subheader("🔍 Search Candidates")

    position_filter = st.text_input("Position Looking For")
    city_filter = st.text_input("City")

    filtered_df = df.copy()

    if position_filter:
        filtered_df = filtered_df[
            filtered_df["position"]
            .str.contains(position_filter, case=False, na=False)
        ]

    if city_filter:
        filtered_df = filtered_df[
            filtered_df["city"]
            .str.contains(city_filter, case=False, na=False)
        ]

    # Candidate Directory
    st.subheader("📋 Candidate Directory")

    display_df = filtered_df[
        [
            "name",
            "city",
            "designation",
            "experience",
            "qualification",
            "position",
            "skills"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # CSV Download
    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📊 Download Candidate Directory (CSV)",
        data=csv,
        file_name="TalentVault_Candidates.csv",
        mime="text/csv"
    )

    st.divider()

    # Resume Downloads
    st.subheader("📄 Download Candidate CVs")

    for _, row in filtered_df.iterrows():

        st.markdown(
            f"**{row['name']}** | "
            f"{row['designation']} | "
            f"{row['experience']} Years | "
            f"{row['city']}"
        )

        resume_path = row["resume_path"]

        if pd.notna(resume_path) and os.path.exists(resume_path):

            with open(resume_path, "rb") as file:

                st.download_button(
                    label=f"Download CV - {row['name']}",
                    data=file.read(),
                    file_name=os.path.basename(resume_path),
                    mime="application/pdf",
                    key=f"cv_{row['id']}"
                )

        else:
            st.warning(
                f"Resume not found for {row['name']}"
            )

        st.divider()

elif password:
    st.error("Invalid Access Code")

else:
    st.info("Enter Employer Access Code to continue.")