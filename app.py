import streamlit as st
import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils import LanguageLoader

# Load environment variables from .env file
load_dotenv()

# 1. Page Configuration & Title
st.set_page_config(page_title="Bambili Language Tutor", page_icon="🇨🇲")
st.title("🇨🇲 Bambili AI Learning Companion")
st.write("Translate, learn, and grow your local language dictionary.")

# 2. Setup Google AI Studio API Client
if "GEMINI_API_KEY" not in os.environ:
    st.error("⚠️ Please set your GEMINI_API_KEY in the .env file.")
    st.info("Create a .env file with: GEMINI_API_KEY=your-key-here")
    st.stop()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 3. Initialize Language Loader
loader = LanguageLoader()
available_languages = loader.get_available_languages()

# Language selection (for future multi-language support)
current_language = "bambili"  # Default for now

# Load language data
try:
    bambili_data = loader.load_language_data(current_language)
except Exception as e:
    st.error(f"Error loading language data: {e}")
    st.stop()

# 4. Sidebar: Teach the AI New Words (Continuous Improvement)
st.sidebar.header("📝 Teach the AI New Skills")
st.sidebar.write(f"📊 Dictionary size: {loader.get_total_words(current_language)} words")

# Category selection for adding new words
category = st.sidebar.selectbox(
    "Category:",
    ["basic_words", "pronouns", "verbs", "nouns"]
)

new_eng = st.sidebar.text_input("English word/phrase:")
new_bam = st.sidebar.text_input("Bambili Translation:")

if st.sidebar.button("Add to Dictionary"):
    if new_eng and new_bam:
        success = loader.save_dictionary_entry(current_language, category, new_eng, new_bam)
        if success:
            st.sidebar.success(f"✅ Added: '{new_eng}' → '{new_bam}' ({category})")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to add entry")

# Language info
if bambili_data.get("metadata"):
    meta = bambili_data["metadata"]
    with st.sidebar.expander("ℹ️ Language Info"):
        st.write(f"**Language:** {meta.get('language_name', 'Bambili')}")
        st.write(f"**Region:** {meta.get('region', 'Cameroon')}")
        st.write(f"**Family:** {meta.get('language_family', 'Niger-Congo')}")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Chat Input Logic
if user_prompt := st.chat_input("Ask me to translate or talk to me..."):
    # Render user message
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Prepare Context to feed into Gemini
    context_injection = loader.format_for_ai_context(current_language)
    
    full_prompt = f"""
{context_injection}

INSTRUCTIONS:
- You are a patient and helpful Bambili language tutor
- The user speaks English and wants to learn Bambili
- Use the dictionary, phrases, and grammar rules provided above
- If a word/phrase is not in the knowledge base, say "I don't have that translation yet. You can add it using the sidebar!"
- Provide literal meanings and cultural context when helpful
- Explain grammar rules when relevant
- Be encouraging and supportive

USER QUESTION: {user_prompt}
"""

    # Generate Response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Translating..."):
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash-latest',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a Bambili language tutor helping English speakers learn Bambili. Use only the provided knowledge base. Be accurate and helpful.",
                        temperature=0.3
                    )
                )
                ai_text = response.text
                st.write(ai_text)
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
            except Exception as e:
                st.error(f"Error calling Gemini: {e}")
                st.info("💡 Tip: Check that your API key is valid at https://makersuite.google.com/app/apikey")
