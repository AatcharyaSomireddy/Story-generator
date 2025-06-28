import streamlit as st
import requests
import json
import os
import time
import re

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="GenAI Story Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .story-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    .story-text {
        font-family: 'Georgia', serif;
        font-size: 18px;
        line-height: 1.6;
        color: #2c3e50;
        text-align: justify;
        white-space: pre-line;
    }
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid #eee;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    .story-stats {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 14px;
        color: #1565c0;
    }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Remove default streamlit padding/margins that create white boxes */
    .block-container {
        padding-top: 1rem;
    }
    
    /* Ensure no extra spacing */
    .stSelectbox, .stTextInput, .stTextArea {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 300;">GenAI Story Generator</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">by Abi Karimireddy</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# API Configuration
# -------------------------------
def get_api_credentials():
    return {
        "api_key": os.getenv("IBM_API_KEY", "your-api-key"),
        "project_id": os.getenv("IBM_PROJECT_ID", "your-project-id"),
        "region": os.getenv("IBM_REGION", "us-south")
    }

CREDENTIALS = get_api_credentials()
VERSION = "2023-05-29"

MODEL_OPTIONS = {
    "Google Flan-UL2": "google/flan-ul2",
    "IBM Granite-13B": "ibm/granite-13b-instruct-v2",
    "Meta Llama-2-70B": "meta-llama/llama-2-70b-chat",
    "Google Flan-T5-XXL": "google/flan-t5-xxl"
}

# -------------------------------
# Enhanced Prompt Builder
# -------------------------------
def create_enhanced_story_prompt(character_name, story_type, context, writing_style, length_category, mood, setting):
    story_structures = {
        "suspense": {
            "opening": "Create an atmosphere of tension and uncertainty",
            "development": "Build suspense through pacing, foreshadowing, and mystery",
            "climax": "Reveal the truth with maximum impact",
            "resolution": "Provide a satisfying conclusion that ties up loose ends"
        },
        "adventure": {
            "opening": "Establish the quest or journey",
            "development": "Present challenges and obstacles to overcome",
            "climax": "Face the greatest challenge or enemy",
            "resolution": "Achieve the goal and show character growth"
        },
        "fantasy": {
            "opening": "Introduce the magical world and its rules",
            "development": "Explore magical elements and their consequences",
            "climax": "Confront the magical threat or complete the quest",
            "resolution": "Restore balance to the magical world"
        },
        "drama": {
            "opening": "Establish character relationships and conflicts",
            "development": "Deepen emotional conflicts and character development",
            "climax": "Face the emotional crisis or life-changing moment",
            "resolution": "Show character growth and resolution of conflicts"
        },
        "mystery": {
            "opening": "Present the mystery or crime to be solved",
            "development": "Gather clues and red herrings, build intrigue",
            "climax": "Reveal the solution and confront the perpetrator",
            "resolution": "Explain the mystery and show justice served"
        },
        "horror": {
            "opening": "Establish normalcy before introducing the supernatural threat",
            "development": "Escalate fear through psychological and physical terror",
            "climax": "Confront the ultimate horror",
            "resolution": "Survive or succumb to the horror with lasting impact"
        }
    }
    
    structure = story_structures.get(story_type.lower(), story_structures["adventure"])
    
    prompt = f"""You are a professional creative writer. Write a compelling {story_type.lower()} story following these specifications:

STORY REQUIREMENTS:
- Main Character: {character_name}
- Genre: {story_type}
- Setting: {setting}
- Mood/Tone: {mood}
- Writing Style: {writing_style}
- Length: {length_category}

STORY CONTEXT:
{context}

STRUCTURE TO FOLLOW:
- Opening: {structure['opening']}
- Development: {structure['development']}
- Climax: {structure['climax']}
- Resolution: {structure['resolution']}

WRITING GUIDELINES:
1. Create vivid, immersive descriptions that engage the senses
2. Develop realistic, relatable characters with clear motivations
3. Use natural, engaging dialogue that reveals character personality
4. Show don't tell - use actions and dialogue to convey emotions
5. Maintain consistent pacing appropriate to the genre
6. Include specific details that bring scenes to life
7. Create emotional resonance with the reader
8. Ensure plot events flow logically and build upon each other
9. Use varied sentence structure for engaging prose
10. End with a satisfying conclusion that feels earned

Write a complete, well-structured story that captures the reader's attention from the first sentence and maintains engagement throughout. Focus on quality storytelling with rich descriptions, compelling characters, and a satisfying narrative arc.

Story:"""

    return prompt

# -------------------------------
# Enhanced IBM Watson API Integration
# -------------------------------
def generate_story_with_watson(prompt, model_id, max_tokens=500, temperature=0.7, creativity_settings=None):
    token = get_iam_token(CREDENTIALS["api_key"])
    if not token:
        return "Error: Could not authenticate with IBM Watson. Please check your API credentials."

    try:
        url = f"https://{CREDENTIALS['region']}.ml.cloud.ibm.com/ml/v1/text/generation?version={VERSION}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "model": model_id,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        # Merge creativity_settings if provided and valid
        if creativity_settings and isinstance(creativity_settings, dict):
            payload.update(creativity_settings)

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()

        # Adjust based on the actual response structure; here is a common pattern
        generated_text = result.get("generated_text")
        if not generated_text:
            # Sometimes the text is under 'choices' -> first item -> 'text'
            generated_text = result.get("choices", [{}])[0].get("text", "No story generated.")

        return generated_text

    except requests.RequestException as e:
        st.error(f"API request error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None
