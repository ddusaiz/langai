import streamlit as st
import json
import os
import time
import random
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from utils import LanguageLoader

# Load environment variables from .env file
load_dotenv()

# 1. Page Configuration & Title
st.set_page_config(page_title="Bambili Language Tutor", page_icon="🇨🇲", layout="wide")
st.title("🇨🇲 Bambili AI Learning Companion")
st.write("Translate, learn, and grow your local language dictionary.")

# 2. Setup Google AI Studio API Client
if "GEMINI_API_KEY" not in os.environ:
    st.error("⚠️ Please set your GEMINI_API_KEY in the .env file.")
    st.info("Create a .env file with: GEMINI_API_KEY=your-key-here")
    st.stop()

api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

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

# Word of the Day Feature
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Word of the Day")

def get_word_of_the_day(language_data):
    """Get a consistent word for today based on date."""
    # Collect all words from dictionary
    all_words = []
    dictionary = language_data.get("dictionary", {})
    
    for category_name, category_data in dictionary.items():
        if isinstance(category_data, dict):
            for eng, bam in category_data.items():
                if bam and bam != "tbd" and bam != "":
                    all_words.append({
                        "english": eng,
                        "bambili": bam,
                        "category": category_name
                    })
    
    if not all_words:
        return None
    
    # Use today's date as seed for consistent daily word
    today = datetime.now().strftime("%Y-%m-%d")
    random.seed(today)
    word = random.choice(all_words)
    random.seed()  # Reset seed
    
    return word

word_of_day = get_word_of_the_day(bambili_data)

if word_of_day:
    st.sidebar.success(f"**{word_of_day['english'].title()}**")
    st.sidebar.write(f"🇨🇲 **{word_of_day['bambili']}**")
    st.sidebar.caption(f"_{word_of_day['category'].replace('_', ' ').title()}_")
else:
    st.sidebar.info("Add more words to see Word of the Day!")

st.sidebar.markdown("---")

# Category selection for adding new words
category_type = st.sidebar.selectbox(
    "Add to:",
    ["Dictionary", "Grammar"]
)

if category_type == "Dictionary":
    category = st.sidebar.selectbox(
        "Category:",
        ["basic_words", "nouns", "greetings", "common_expressions", "polite_expressions",
         "numbers", "colors", "body_parts", "family", "time_expressions", 
         "common_verbs", "adjectives", "animals", "nature"]
    )
else:
    category = st.sidebar.selectbox(
        "Category:",
        ["pronouns", "verbs"]
    )

new_eng = st.sidebar.text_input("English word/phrase:")
new_bam = st.sidebar.text_input("Bambili Translation:")

if st.sidebar.button("Add Entry"):
    if new_eng and new_bam:
        # Save to appropriate file based on category type
        if category_type == "Grammar":
            success = loader.save_grammar_entry(current_language, category, new_eng, new_bam)
        else:
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

# 5. Create Tabs for Different Modes
tab1, tab2, tab3 = st.tabs(["💬 AI Chat Tutor", "🎭 Conversation Practice", "📚 Dictionary Browser"])

# TAB 1: AI Chat Tutor (Original functionality)
with tab1:
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display old messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input Logic
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
                    # Create the model - using gemini-flash-latest (stable and available)
                    model = genai.GenerativeModel('gemini-flash-latest')
                    
                    # Generate response (non-streaming for reliability)
                    response = model.generate_content(full_prompt)
                    ai_text = response.text
                    
                    st.write(ai_text)
                    st.session_state.messages.append({"role": "assistant", "content": ai_text})
                    
                    # Small delay to prevent rapid-fire requests
                    time.sleep(0.5)
                    
                except Exception as e:
                    error_msg = str(e)
                    
                    # Check for rate limit error (429)
                    if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                        st.error("⚠️ **Rate Limit Exceeded (Error 429)**")
                        st.warning("**You've made too many requests!**")
                        st.info("""
**What to do:**
1. ⏰ **Wait 1-5 minutes** and try again
2. 🎭 Use the **Conversation Practice** tab (no API needed!)
3. 📚 Use the **Dictionary Browser** tab (no API needed!)
4. 🔑 Check your quota: https://aistudio.google.com/app/apikey

**Tips to avoid this:**
- Don't send messages too quickly
- Wait a few seconds between requests
- Consider upgrading to a paid plan for higher limits
                        """)
                    else:
                        st.error(f"Error calling Gemini: {error_msg}")
                        st.info("💡 Make sure your API key is valid at https://aistudio.google.com/app/apikey")

# TAB 2: Conversation Practice
with tab2:
    st.header("🎭 Practice Real Conversations")
    st.write("Select a scenario below to practice common situations in Bambili")
    
    # Load conversation scenarios
    conversations_path = f"languages/{current_language}/conversations.json"
    if os.path.exists(conversations_path):
        with open(conversations_path, 'r', encoding='utf-8') as f:
            conversations_data = json.load(f)
        
        scenarios = conversations_data.get("scenarios", [])
        
        # Scenario selector
        col1, col2 = st.columns([2, 1])
        
        with col1:
            scenario_options = {s["title"]: s for s in scenarios}
            selected_title = st.selectbox(
                "Choose a conversation scenario:",
                options=list(scenario_options.keys())
            )
        
        with col2:
            practice_mode = st.radio("Practice Mode:", ["Learn", "Quiz Me"])
        
        if selected_title:
            scenario = scenario_options[selected_title]
            
            # Display scenario info
            st.subheader(scenario["title"])
            st.write(f"**Description:** {scenario['description']}")
            st.write(f"**Difficulty:** {scenario['difficulty'].capitalize()}")
            
            # Cultural note
            if "cultural_note" in scenario:
                st.info(f"💡 **Cultural Note:** {scenario['cultural_note']}")
            
            st.divider()
            
            if practice_mode == "Learn":
                # Show full dialogue
                st.write("### 📖 Full Conversation")
                for i, line in enumerate(scenario["dialogue"]):
                    with st.container():
                        col1, col2, col3 = st.columns([1, 2, 2])
                        with col1:
                            speaker_emoji = "👤" if line["speaker"] == "You" else "👥"
                            st.write(f"**{speaker_emoji} {line['speaker']}:**")
                        with col2:
                            st.write(f"🇬🇧 {line['english']}")
                        with col3:
                            st.write(f"🇨🇲 **{line['bambili']}**")
                            if "audio_note" in line:
                                st.caption(f"🔊 {line['audio_note']}")
                    if i < len(scenario["dialogue"]) - 1:
                        st.write("")
                
                # Vocabulary section
                if "vocabulary" in scenario:
                    st.divider()
                    st.write("### 📝 Key Vocabulary")
                    st.write(", ".join(scenario["vocabulary"]))
            
            else:  # Quiz Mode
                # Initialize quiz state
                if "quiz_index" not in st.session_state:
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.show_answer = False
                
                st.write("### 🎯 Quiz Mode")
                st.write("Try to translate the sentences!")
                
                dialogue = scenario["dialogue"]
                current_index = st.session_state.quiz_index
                
                if current_index < len(dialogue):
                    line = dialogue[current_index]
                    
                    st.write(f"**{line['speaker']} says:**")
                    st.write(f"### 🇬🇧 {line['english']}")
                    st.write("Translate to Bambili:")
                    
                    user_answer = st.text_input("Your translation:", key=f"quiz_{current_index}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("Show Answer"):
                            st.session_state.show_answer = True
                    
                    with col2:
                        if st.button("Next →"):
                            st.session_state.quiz_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
                    
                    with col3:
                        if st.button("Reset Quiz"):
                            st.session_state.quiz_index = 0
                            st.session_state.quiz_score = 0
                            st.session_state.show_answer = False
                            st.rerun()
                    
                    if st.session_state.show_answer:
                        st.success(f"✅ Correct answer: **{line['bambili']}**")
                        if "audio_note" in line:
                            st.info(f"🔊 Pronunciation: {line['audio_note']}")
                    
                    # Progress
                    st.progress((current_index + 1) / len(dialogue))
                    st.caption(f"Question {current_index + 1} of {len(dialogue)}")
                else:
                    st.success("🎉 You completed this conversation!")
                    if st.button("Try Again"):
                        st.session_state.quiz_index = 0
                        st.session_state.show_answer = False
                        st.rerun()
    else:
        st.warning("Conversation scenarios not found. Please create conversations.json")

# TAB 3: Dictionary Browser
with tab3:
    st.header("📚 Browse Dictionary")
    
    # Get all dictionary data
    dictionary = bambili_data.get("dictionary", {})
    grammar = bambili_data.get("grammar", {})
    
    # Search functionality
    search_term = st.text_input("🔍 Search for a word:", placeholder="Enter English word...")
    
    if search_term:
        st.write(f"### Results for '{search_term}'")
        found = False
        
        # Search in dictionary
        for category_name, category_data in dictionary.items():
            if isinstance(category_data, dict):
                for eng, bam in category_data.items():
                    if search_term.lower() in eng.lower():
                        st.write(f"- **{eng}** → {bam} _{category_name}_")
                        found = True
        
        # Search in grammar
        for category_name in ["pronouns", "verbs"]:
            if category_name in grammar:
                for eng, bam in grammar[category_name].items():
                    if search_term.lower() in eng.lower():
                        st.write(f"- **{eng}** → {bam} _{category_name}_")
                        found = True
        
        if not found:
            st.info("No results found. You can add this word using the sidebar!")
    else:
        # Browse by category
        st.write("### Browse by Category")
        
        category_to_show = st.selectbox(
            "Select category:",
            options=list(dictionary.keys()) + ["pronouns", "verbs"]
        )
        
        if category_to_show in dictionary:
            data = dictionary[category_to_show]
        elif category_to_show in grammar:
            data = grammar[category_to_show]
        else:
            data = {}
        
        if data:
            st.write(f"#### {category_to_show.replace('_', ' ').title()}")
            
            # Display in columns
            col1, col2 = st.columns(2)
            items = list(data.items())
            mid = len(items) // 2
            
            with col1:
                for eng, bam in items[:mid]:
                    st.write(f"• **{eng}** → {bam}")
            
            with col2:
                for eng, bam in items[mid:]:
                    st.write(f"• **{eng}** → {bam}")
        else:
            st.info("No entries in this category yet.")
 
 