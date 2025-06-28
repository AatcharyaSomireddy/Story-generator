import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Story Generator")

prompt = st.text_input("Enter your story prompt:")

if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating story..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a creative storyteller."},
                    {"role": "user", "content": prompt},
                ],
            )
            story = response.choices[0].message.content
            st.markdown("### Your Story:")
            st.write(story)
    else:
        st.warning("Please enter a prompt.")
