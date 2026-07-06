# 🇨🇲 Bambili Language Learning App

An AI-powered language learning companion built with Streamlit and Google's Gemini API. Help English speakers learn Bambili, a Grassfields Bantu language spoken in Cameroon.

## 🌟 Features

- **Interactive AI Tutor**: Chat with an AI tutor powered by Google Gemini
- **Comprehensive Dictionary**: Browse and search words by category
- **Grammar Rules**: Learn sentence structure and grammar patterns
- **Common Phrases**: Practice greetings and everyday expressions
- **Expandable Learning**: Add new words and phrases to the knowledge base
- **Multi-language Ready**: Extensible architecture for adding more languages

## 📁 Project Structure

```
bambili-agent/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── utils/
│   ├── __init__.py
│   └── language_loader.py      # Language data management utilities
└── languages/
    ├── config.json             # Languages configuration
    └── bambili/                # Bambili language data
        ├── metadata.json       # Language metadata
        ├── dictionary.json     # Word translations by category
        ├── phrases.json        # Common phrases and expressions
        └── grammar.json        # Grammar rules and examples
```

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd /Users/P/projects/bambili-agent
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv env
source env/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root:

```bash
echo 'GEMINI_API_KEY=your-actual-api-key-here' > .env
```

Or manually create `.env` with:
```
GEMINI_API_KEY=your-actual-api-key-here
```

**Get your API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📚 Language Data Organization

### Adding a New Language

To add support for another language (e.g., French, Spanish, another African language):

1. Create a new folder: `languages/your_language_code/`
2. Add the required JSON files:
   - `metadata.json` - Language info
   - `dictionary.json` - Word categories
   - `phrases.json` - Common expressions
   - `grammar.json` - Grammar rules
3. Update `languages/config.json` to include the new language
4. Use the language selector in the app

### Dictionary Structure

Organize words by category for better learning:

```json
{
  "basic_words": { "hello": "translation", ... },
  "pronouns": { "I": "translation", ... },
  "verbs": { "eat": "translation", ... },
  "nouns": { "water": "translation", ... }
}
```

### Phrases Structure

Group phrases by context:

```json
{
  "greetings": [
    {
      "english": "Good morning",
      "bambili": "abi mwuah",
      "literal_meaning": "it's day break",
      "context": "Used in the morning"
    }
  ],
  "common_expressions": [...],
  "polite_expressions": [...]
}
```

### Grammar Structure

Define clear rules with examples:

```json
{
  "sentence_structure": {
    "basic_order": "Subject-Verb-Object",
    "description": "...",
    "examples": [...]
  },
  "grammar_rules": [
    {
      "rule_id": "unique_id",
      "title": "Rule Title",
      "description": "Explanation",
      "examples": [...]
    }
  ]
}
```

## 🔧 Usage

### Learning Mode
- Ask the AI tutor questions like:
  - "How do I say 'hello' in Bambili?"
  - "Translate 'good morning' to Bambili"
  - "Explain the sentence structure"
  - "What are the pronouns?"

### Teaching Mode
- Use the sidebar to add new vocabulary
- Select a category (basic_words, verbs, etc.)
- Enter English and Bambili translations
- Click "Add to Dictionary"

### Browse Data
- Check the sidebar for:
  - Total dictionary size
  - Language information
  - Quick reference

## 🛠️ Customization

### Modify AI Behavior

Edit the system instruction in `app.py`:

```python
system_instruction="You are a Bambili language tutor..."
```

### Adjust AI Creativity

Change the `temperature` parameter (0.0 = focused, 1.0 = creative):

```python
temperature=0.3
```

### Add More Categories

Update the category dropdown in `app.py`:

```python
category = st.sidebar.selectbox(
    "Category:",
    ["basic_words", "pronouns", "verbs", "nouns", "adjectives", "numbers"]
)
```

## 🌍 Extensibility

This project is designed for easy expansion:

1. **More African Languages**: Add Swahili, Yoruba, Zulu, etc.
2. **Audio Support**: Integrate text-to-speech for pronunciation
3. **Quizzes**: Add interactive exercises and tests
4. **Progress Tracking**: Store user learning history
5. **Community Features**: Allow users to share custom phrases
6. **Mobile App**: Convert to a mobile-friendly PWA

## 📝 Contributing

To add content to the Bambili knowledge base:

1. Fill in `tbd` (to be determined) entries in the JSON files
2. Add more grammar rules with examples
3. Expand the dictionary with more categories
4. Add cultural context to phrases

## 🔐 Security Note

- Never commit your `.env` file to version control
- Keep your API keys private
- Add `.env` to your `.gitignore` file

## 📄 License

This project is for educational purposes. Please respect the cultural heritage of the Bambili language and its speakers.

## 🙏 Acknowledgments

Built with love for language preservation and learning. Special thanks to the Bambili-speaking community in Cameroon.
