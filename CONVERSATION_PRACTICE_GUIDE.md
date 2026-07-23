# 🎭 Conversation Practice Mode - User Guide

## What's New?

Your Bambili Language Learning App now has **3 tabs**:

### 1. 💬 AI Chat Tutor
- Original chat functionality with Gemini AI
- Ask questions, get translations
- Conversational learning

### 2. 🎭 Conversation Practice (NEW!)
- Pre-built realistic conversation scenarios
- Two modes: **Learn** and **Quiz Me**
- Cultural notes and pronunciation guides

### 3. 📚 Dictionary Browser (NEW!)
- Search functionality for quick lookups
- Browse words by category
- Easy reference tool

---

## How to Use Conversation Practice

### Learn Mode
1. Select a conversation scenario from the dropdown
2. Choose "Learn" mode
3. Read through the full dialogue with:
   - English translation
   - Bambili translation
   - Pronunciation guide
   - Cultural context

### Quiz Mode
1. Select a conversation scenario
2. Choose "Quiz Me" mode
3. Try to translate each English sentence to Bambili
4. Click "Show Answer" to check your translation
5. Use "Next" to move to the next sentence
6. Track your progress with the progress bar

---

## Available Scenarios

1. **🙏 Greeting an Elder** (Beginner)
   - Learn respectful greetings
   - Cultural etiquette with elders

2. **🛒 At the Market** (Intermediate)
   - Shopping vocabulary
   - Bargaining basics

3. **👋 Introducing Yourself** (Beginner)
   - Name exchanges
   - Basic introductions

4. **🗺️ Asking for Directions** (Intermediate)
   - Navigation vocabulary
   - Understanding directions

5. **🍽️ Ordering Food** (Beginner)
   - Food vocabulary
   - Restaurant phrases

---

## Adding Your Own Scenarios

Edit `languages/bambili/conversations.json` to add new scenarios:

```json
{
  "id": "your_scenario_id",
  "title": "🎯 Your Scenario Title",
  "description": "What this scenario teaches",
  "difficulty": "beginner",
  "dialogue": [
    {
      "speaker": "You",
      "english": "English phrase",
      "bambili": "Bambili translation",
      "audio_note": "pronunciation guide"
    }
  ],
  "vocabulary": ["key", "words"],
  "cultural_note": "Cultural context or tips"
}
```

---

## Tips for Best Results

1. **Start with Beginner scenarios** - Build confidence first
2. **Use Learn mode first** - Familiarize yourself with the dialogue
3. **Practice pronunciation** - Read the audio notes out loud
4. **Try Quiz mode** - Test your memory
5. **Read cultural notes** - Context helps with retention
6. **Add new words** - Use the sidebar to expand the dictionary

---

## Future Enhancements Ideas

- Audio playback for pronunciations
- Voice input for practice
- Spaced repetition reminders
- Track completion progress
- Certificate after completing all scenarios
- Community-contributed scenarios

---

## Running the App

```bash
streamlit run app.py
```

Then click on the **🎭 Conversation Practice** tab!

Enjoy learning Bambili! 🇨🇲
