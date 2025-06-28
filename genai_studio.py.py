import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Story Generator", layout="centered")

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("📚 AI Story Generator")

genre = st.selectbox("Choose a genre:", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Adventure"])
character = st.text_input("Main character's name:")
setting = st.text_input("Setting (optional):")
length = st.slider("Length of story (approx. words)", 100, 1000, 300)

if st.button("Generate Story"):
    prompt = f"Write a {genre.lower()} story about {character}"
    if setting:
        prompt += f" set in {setting}"
    prompt += f". The story should be around {length} words."

    with st.spinner("Generating story..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # or "gpt-4", "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are a creative story writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=int(length * 1.3),  # safe estimate
            )
            story = response.choices[0].message.content
            st.subheader("Your AI-Generated Story:")
            st.write(story)
        except Exception as e:
            st.error(f"Error: {e}")
